import pyodbc
from typing import List
import logging
from typing import Tuple
from collections import namedtuple
from enum import Enum
from datetime import datetime
import re

from sql.config import CONN_STR
from configs.lauch_config import ReplacementPattern
from sql.sql_templates import GET_COLUMNS, MERGE_STM, MERGE_SP, PULL_SP, or_alter
import sql.naming_convention as nc
from sql.code_transformations import apply_mappings, apply_sql_formating
import sql.output_to as outo

ColumnInfo = namedtuple('ColumnInfo', ['column_name',
                                       'data_type',
                                       'precision',
                                       'scale',
                                       'is_nullable',
                                       'is_identity',
                                       'seed_value',
                                       'increment_value',
                                       'default_constr',
                                       'check_constr',
                                       'is_in_pk'
                                       ])

SQL_GO = "\nGO\n"


class SQL_OBJECT_TYPE(Enum):
    TABLE = 1
    STG_TABLE = 2
    VIEW = 3
    PULL_SP = 4
    MERGE_SP = 5


class SQL_Communicator:
    def __enter__(self):
        self.conn_str = CONN_STR
        logging.info(self.conn_str)
        print('connecting...')
        self.connection = pyodbc.connect(self.conn_str, timeout=60)
        print("Connection successful!")
        return self

    def get_execution_metrics(self, stm: str):
        tm0 = datetime.now()
        cursor = self.connection.cursor()   
        cursor.execute(stm)
        time_dif = datetime.now() - tm0
        return time_dif

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.connection.close()

    def get_columns(self, table_name: str) -> List[ColumnInfo]:
        conn = self.connection
        cursor = conn.cursor()
        query = GET_COLUMNS.format(table_name=table_name)        
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [ColumnInfo(
            row.column_name,
            row.data_type,
            row.precision,
            row.scale,
            row.is_nullable,
            row.is_identity,
            row.seed_value,
            row.increment_value,
            row.default_constr,
            row.check_constr,
            row.is_pk)
            for row in rows]
        cursor.close()

        if not columns:
            ex_mess = f'looks like table {table_name} has not been created yet'
            raise Exception(ex_mess)

        return columns

    def get_sql_object_id(self, object_name: str):
        conn = self.connection
        cursor = conn.cursor()
        cursor.execute(f"SELECT OBJECT_ID('{object_name}')")
        r = cursor.fetchone()
        cursor.close()
        if r[0]:
            return int(r[0])

    def get_module_def(self, object_name: str) -> str:
        """
        Gets the definition of a SQL Server view or stored procedure.        
        Args:
            cursor (pyodbc.Cursor): The database cursor.
            object_name (str): The name of the view or stored procedure.            
        Returns:
            str: The definition of the view or stored procedure.
        """
        query = f"SELECT definition FROM sys.sql_modules WHERE object_id = OBJECT_ID('{object_name}');"
        conn = self.connection
        cursor = conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row[0]

    def clone_view(self, entity_name: str,
                   nc_view_name: callable = nc.source_view_name,
                   rppts: List[ReplacementPattern] = None):
        nc_view_name = nc_view_name or nc.source_view_name  # default naming conv for view name                    
        view_name = nc_view_name(entity_name)
        vid = self.get_sql_object_id(view_name)
        if not vid:
            logging.info(f'View {view_name} was not found')
            nc_view_name = nc.view_name
            view_name = nc_view_name(entity_name)
            vid = self.get_sql_object_id(view_name)
        if not vid:
            logging.warning(f'View {view_name} was not found as well. Have to skip view creation')
            return None, None

        view_name = view_name.split('.')[-1]  # to eliminate schema name
        view_name2 = nc_view_name(nc.default_rename(entity_name)).split('.')[-1]

        view_def = self.get_module_def(view_name)
        #  print(view_def)
        if rppts:
            view_def = apply_mappings(view_def, rppts)  # applying some code replacemements, defined in congigs
        view_def = apply_sql_formating(view_def)
        view_def = re.sub(view_name, view_name2, view_def, flags=re.IGNORECASE) + SQL_GO
        return view_def, view_name2

    def generate_merge_stm(self, tbl_srs: str, tbl_dst: str) -> str:
        cols = self.get_columns(table_name=tbl_dst)
        insrt = ', '.join([x.column_name for x in cols])
        insrt2 = ', '.join([f'SRC.{x.column_name}' for x in cols])

        join_cond = ' AND '.join([f'DST.{x.column_name} = SRC.{x.column_name}' for x in cols if x.is_in_pk])
        non_pk_cols = [x.column_name for x in cols if not x.is_in_pk]
        update_part = ',\n'.join([f'{x} = SRC.{x}' for x in non_pk_cols])
        update_cond = ' AND '.join([f"ISNULL(DST.{x}, 0) <> ISNULL(SRC.{x}, 0) " for x in non_pk_cols])
        stm = MERGE_STM.format(tbl_dst=tbl_dst, tbl_srs=tbl_srs, join_cond=join_cond, update_cond=update_cond,
                               update_part=update_part, insrt=insrt, insrt2=insrt2)
        return stm

    def generate_insert_stm(self, view_srs: str, tbl_dst: str) -> str:
        cols = self.get_columns(table_name=tbl_dst)
        cols_str = ','.join([x.column_name for x in cols])

        return f"""INSERT INTO {tbl_dst} ({cols_str})
        SELECT {cols_str} FROM {view_srs}"""

    def create_merge_sp(self, entity_name, entity_name2=None, create_or_alter=True):
        entity_name2 = entity_name2 or nc.default_rename(entity_name)
        sp_name = nc.merge_sp_name(entity_name=entity_name2)
        trg_table = nc.table_name(entity_name2)
        stg_tbl = nc.stg_table_name(entity_name)
        merge_stm = self.generate_merge_stm(tbl_srs=stg_tbl, tbl_dst=trg_table)
        create_sp_stm = MERGE_SP.format(sp_name=sp_name, merge_stm=merge_stm, or_alter=or_alter(create_or_alter))
        create_sp_stm = apply_sql_formating(create_sp_stm)
        return create_sp_stm, sp_name
  
    def create_pull_sp(self, entity_name, entity_name2=None, source_view_name=None, create_or_alter=True):
        entity_name2 = entity_name2 or nc.default_rename(entity_name)
        source_view_name = source_view_name or nc.source_view_name(entity_name)
        sp_name = nc.pull_sp_name(entity_name=entity_name2)
        dst_tbl = nc.stg_table_name(entity_name)
        ins_stm = self.generate_insert_stm(source_view_name, dst_tbl)
        create_sp_stm = PULL_SP.format(sp_name=sp_name, table_name=dst_tbl, ins_stm=ins_stm, 
                                       or_alter=or_alter(create_or_alter))
        create_sp_stm = apply_sql_formating(create_sp_stm)                              
        return create_sp_stm, sp_name

    def get_table_definition(self, table_name, new_table_name: str = None):
        schema_name, table_name = extract_schema_and_table_names(table_name)

        column_query = f"""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{schema_name}'
        """

        pk_query = f"""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + CONSTRAINT_NAME), 'IsPrimaryKey') = 1
            AND TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{schema_name}'
        """

        fk_query = f"""
            SELECT KCU.COLUMN_NAME, KCU2.TABLE_NAME AS REFERENCED_TABLE_NAME, KCU2.COLUMN_NAME AS REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS RC
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU ON KCU.CONSTRAINT_NAME = RC.CONSTRAINT_NAME
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU2 ON KCU2.CONSTRAINT_NAME = RC.UNIQUE_CONSTRAINT_NAME
            WHERE KCU.TABLE_NAME = '{table_name}' AND KCU.TABLE_SCHEMA = '{schema_name}'
        """

        index_query = f"""
            SELECT IX.name AS index_name, COL.name AS column_name, IX.type_desc, IX.is_unique, IX.fill_factor
            FROM sys.indexes IX
            JOIN sys.index_columns IC ON IX.object_id = IC.object_id AND IX.index_id = IC.index_id
            JOIN sys.columns COL ON IC.object_id = COL.object_id AND IC.column_id = COL.column_id
            JOIN sys.tables TBL ON IX.object_id = TBL.object_id
            JOIN sys.schemas SCH ON TBL.schema_id = SCH.schema_id
            WHERE TBL.name = '{table_name}' AND SCH.name = '{schema_name}'
        """
        connection = self.connection

        with connection.cursor() as cursor:
            cursor.execute(column_query)
            columns = cursor.fetchall()
            if not columns:
                raise Exception(f'Looks like table {schema_name}.{table_name} does not exist in DB')

            cursor.execute(pk_query)
            primary_keys = [row[0] for row in cursor.fetchall()]
            
            cursor.execute(fk_query)
            foreign_keys = cursor.fetchall()

            cursor.execute(index_query)
            indexes = cursor.fetchall()

        script = []
        if new_table_name:
            schema_name, table_name = extract_schema_and_table_names(new_table_name)
        script.append(f"CREATE TABLE [{schema_name}].[{table_name}] (")
        
        col_defs = []
        for column in columns:
            col_name, data_type, is_nullable, char_length = column
            col_def = f"    [{col_name}] {data_type}"
            if data_type in ('VARCHAR', 'NVARCHAR', 'CHAR', 'NCHAR') and char_length:
                col_def += f"({char_length})"
            col_def += ' NOT NULL' if is_nullable == 'NO' else ' NULL'
            col_defs.append(col_def)
        script.append(",\n".join(col_defs))

        if primary_keys:
            script.append(f",\n    PRIMARY KEY ({', '.join(primary_keys)})")

        for fk in foreign_keys:
            script.append(f",\n    FOREIGN KEY ([{fk[0]}]) REFERENCES [{fk[1]}]([{fk[2]}])")
        
        script.append("\n);\n")

        for index in indexes:
            unique = 'UNIQUE ' if index.is_unique else ''
            script.append(f"CREATE {unique}{index.type_desc} INDEX [{index.index_name}] ON [{schema_name}].[{table_name}]([{index.column_name}] ASC)")
            if index.fill_factor:
                script.append(f" WITH (FILLFACTOR = {index.fill_factor});")
            else:
                script.append(";")
        
        return "\n".join(script)

    def create_new_sql_object(self, ot: SQL_OBJECT_TYPE, ents: List[str], src_views_ents: List[str] = [], output_dir: str = None,
                              rppts: List[ReplacementPattern] = None): 
        big_script = ''
        source_views = [nc.source_view_name(nc.default_rename(x)) for x in src_views_ents] 
        zz = zip(ents, source_views) if source_views else ents
        for tp in zz:
            # source_view_name, source_view_name = nc.source_view_name(entity_name)
            entity_name = tp[0] if source_views else tp
            source_view_name = tp[1] if source_views else None
            match ot:
                case SQL_OBJECT_TYPE.TABLE:
                    table_name = nc.table_name(entity_name)
                    obj_name = nc.table_name(nc.default_rename(entity_name))
                    obj_def = self.get_table_definition(table_name, obj_name)
                    ot_folder = 'Tables'
                case SQL_OBJECT_TYPE.STG_TABLE:
                    table_name = nc.table_name(entity_name)
                    obj_name = nc.stg_table_name(entity_name)
                    obj_def = self.get_table_definition(table_name, obj_name)
                    ot_folder = 'Tables'
                case SQL_OBJECT_TYPE.VIEW:
                    obj_def, obj_name = self.clone_view(entity_name=entity_name, rppts=rppts)
                    ot_folder = 'Views'
                case SQL_OBJECT_TYPE.PULL_SP:
                    obj_def, obj_name = self.create_pull_sp(entity_name, nc.default_rename(entity_name), source_view_name)
                    ot_folder = 'StoredProcedures'
                case SQL_OBJECT_TYPE.MERGE_SP:
                    obj_def, obj_name = self.create_merge_sp(entity_name, nc.default_rename(entity_name))
                    ot_folder = 'StoredProcedures'
            if obj_name:
                big_script += obj_def + SQL_GO
                if output_dir:
                    outo.output_to_file(output_dir, ot_folder, obj_name, obj_def)
            else:
                logging.warning(f'could not create {ot} for {entity_name}. Skipping.')
        return big_script


def extract_schema_and_table_names(table_name: str) -> Tuple[str, str]:
    sntn = table_name.split('.')
    if len(sntn) > 1:
        schema_name, table_name = sntn[0].strip('[]'), sntn[1].strip('[]')
    else:
        schema_name, table_name = 'dbo', sntn[0].strip('[]')
    return schema_name, table_name

