import pyodbc
from typing import List, Tuple
import logging
from collections import namedtuple
from enum import Enum
from datetime import datetime
import re

import sql.config as sql_config
from sql.data_classes import SQL_Object, DB_Object_Type
from configs.lauch_config import ReplacementPattern
from sql.sql_templates import GET_COLUMNS, MERGE_STM, MERGE_SP, MERGE_STM_WITHOUT_UPDATE, PULL_SP, or_alter, GET_DEPENDENCIES
import sql.naming_convention as nc
from sql.code_transformations import apply_mappings, apply_sql_formating, apply_create_or_alter_view
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
        self.DB_NAME = sql_config.DB_NAME
        self.conn_str = sql_config.CONN_STR
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

    def run_select(self, query: str, is_single_row: bool, *args) -> List[Tuple]:
        conn = self.connection
        cursor = conn.cursor()
        cursor.execute(query, args)
        if is_single_row:
            f = cursor.fetchone()
            ret = [f]
        else:
            ret = cursor.fetchall()
        cursor.close()
        return ret

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
        r = self.run_select(f"SELECT OBJECT_ID('{object_name}')", is_single_row=True)
        if r[0] and r[0][0]:
            return int(r[0][0])

    def get_table_size(self, object_name: str) -> str:
        query = f"""
        SELECT
            SUM(p.rows) AS RowCounts,
            (SUM(a.total_pages) * 8) / 1024.0 as TotalSpaceMB
            FROM sys.tables t
                INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
                INNER JOIN sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
                INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
            WHERE i.OBJECT_ID > 255
            AND i.index_id IN (0,1)
            AND t.object_id = OBJECT_ID('{object_name}');"""

        return self.run_select(query)

    def get_module_def(self, object_name: str) -> str:
        """
        Gets the definition of a SQL Server view or stored procedure.        
        Args:
            object_name (str): The name of the view or stored procedure.            
        Returns:
            str: The definition of the view or stored procedure.
        """
        nnn = parse_db_obj_full_name(object_name)
        db_name = '' if len(nnn) < 3 else nnn[0] + '.'
        query = f"SELECT definition FROM {db_name}sys.sql_modules WHERE object_id = OBJECT_ID('{object_name}');"
        row = self.run_select(query=query, is_single_row=True)
        if row[0] and row[0][0]:
            return row[0][0]

    def get_sql_object(self, object_name: str, schema_name: str = None, db_name: str = None) -> SQL_Object:
        schema_name = schema_name or 'dbo'
        db_name = f'{db_name}.' if db_name else ''        
        query = f"""
        select ob.object_id, ob.name, ob.type_desc, * 
        from {db_name}sys.objects ob 
        join  {db_name}sys.schemas sch on sch.schema_id=ob.schema_id
        where ob.name=? and sch.name=? """
        x = self.run_select(query, True, object_name, schema_name)
        if x:
            x = x[0]
            return SQL_Object(object_id=x[0], name=x[1], type=x[2], schema=schema_name or 'dbo', db_name=db_name)

    def get_object_dependencies(self, object_name: str, is_recursive=False, db_name: str = None, db_object_type: DB_Object_Type = None,
                                level: int = 1) -> List[Tuple[SQL_Object, int]]:
        db_name = f'{db_name}.' if db_name else ''
        query = GET_DEPENDENCIES.format(db_name=db_name)
        tt = self.run_select(query, False, object_name)
        deps = [(SQL_Object(object_id=x[0],
                            type=x[1], name=x[2], schema=x[3] or 'dbo',
                            db_name=x[4], server_name=x[5]),
                level)
                for x in tt]
        for dep, _ in deps:
            if not dep.object_id:  # object from another DB
                xx = self.get_sql_object(dep.name, schema_name=dep.schema, db_name=dep.db_name)
                dep.object_id, dep.type = xx.object_id, xx.type
        if db_object_type:
            deps = [x for x in deps if DB_Object_Type(x[0].type) == db_object_type]
        if is_recursive:
            level += 1
            for so, _ in deps:
                on = f'{so.schema or 'dbo'}.{so.name}'
                deps_next = self.get_object_dependencies(on, is_recursive=is_recursive, db_name=so.db_name, db_object_type=db_object_type,
                                                         level=level)
                deps.extend(deps_next)
        return deps

    def get_view_names(self, entity_name: str, nc_view_name: callable = nc.source_view_name):
        nc_view_name = nc_view_name or nc.source_view_name  # default naming conv for view name                    
        view_name = nc_view_name(entity_name)
        vid = self.get_sql_object_id(view_name)
        if not vid:
            logging.info(f'View {view_name} was not found')
            nc_view_name = nc.view_name
            view_name = nc_view_name(entity_name)
            vid = self.get_sql_object_id(view_name)
        if not vid:
            logging.warning(f'View {view_name} was not found as well')
            return None, None

        view_name = view_name.split('.')[-1]  # to eliminate schema name
        view_name2 = nc_view_name(nc.default_rename(entity_name)).split('.')[-1]
        return view_name, view_name2

    def deep_clone_view(self, view_name: str,
                        view_name2: str,
                        rppts: List[ReplacementPattern] = None) -> List[Tuple[str, str, str, int, str]]:
        """_summary_

        Args:
            view_name (str): view name for cloning
            view_name2 (str): name of cloned view
            rppts (List[ReplacementPattern], optional): patterns of code replacement. Defaults to None.

        Returns:
            List[Tuple]: new_view_def, view_name2, view_name, level, db_name
        """
        ret_lst, level = [], 0

        def deep_clone_view_recursive(view_name: str, view_name2: str, level: int) -> bool:
            level += 1
            # before creation of new definiton need to create all child definitions if necessary
            child_vws = self.get_object_dependencies(object_name=view_name, is_recursive=True, db_object_type=DB_Object_Type.VIEW)
            child_renamings = []
            for vw, _ in child_vws:
                en, suffix = nc.entity_name_from_view_name(vw.name)
                vnc2 = nc.default_rename(en) + suffix
                cnbc = deep_clone_view_recursive(vw.full_name, vnc2, level)
                if cnbc:
                    child_renamings.append((vw.name, vnc2))

            new_view_def, is_replaced, db_name = self.clone_view(view_name, view_name2, rppts)
            clone_need_to_be_created = False
            if new_view_def:
                if not ret_lst or is_replaced or child_renamings:
                    # for first level we do clone any way, for lower -only if we need to replace something in the view itself or in the child view
                    rppts_ref = [ReplacementPattern(re_replace_this=fr'\b{x[0]}\b', replace_to=x[1]) for x in child_renamings]
                    new_view_def = apply_mappings(new_view_def, rppts_ref)
                    ret_lst.append([new_view_def, view_name2, view_name, level, db_name])
                    clone_need_to_be_created = True
            return clone_need_to_be_created

        deep_clone_view_recursive(view_name, view_name2, level)
        return ret_lst

    def clone_view(self, view_name: str,
                   view_name2: str,
                   rppts: List[ReplacementPattern] = None) -> Tuple[str, str, bool, str]:
        view_def = self.get_module_def(view_name).strip()
        if not view_def:
            logging.warn(f'definiton for view {view_name} is not available')
            return None, False
        view_name2 = _create_obj_name_for_replacement(view_name, view_name2)
        view_def = rename_sql_object(view_def, view_name2)
        new_view_def, is_replaced = view_def, False
        #  print(view_def)
        if rppts:
            new_view_def = apply_mappings(view_def, rppts)
            is_replaced = new_view_def != view_def
        new_view_def = apply_create_or_alter_view(new_view_def)
        new_view_def = apply_sql_formating(new_view_def)

        db_name = None
        nnn = parse_db_obj_full_name(view_name)
        if len(nnn) > 2:
            db_name = nnn[-3]
            new_db_name = apply_mappings(db_name, rppts)  # need to replace db names as well
            is_replaced = db_name == new_db_name
            db_name = new_db_name
        return new_view_def + SQL_GO, is_replaced, db_name

    def generate_merge_stm(self, tbl_srs: str, tbl_dst: str) -> str:
        cols = self.get_columns(table_name=tbl_dst)
        insrt = ', '.join([x.column_name for x in cols])
        insrt2 = ', '.join([f'SRC.{x.column_name}' for x in cols])

        join_cond = ' AND '.join([f'DST.{x.column_name} = SRC.{x.column_name}' for x in cols if x.is_in_pk])
        non_pk_cols = [x.column_name for x in cols if not x.is_in_pk]
        if non_pk_cols:
            update_part = ',\n'.join([f'{x} = SRC.{x}' for x in non_pk_cols])
            update_cond = ' AND '.join([f"ISNULL(DST.{x}, 0) <> ISNULL(SRC.{x}, 0) " for x in non_pk_cols])
            stm = MERGE_STM.format(tbl_dst=tbl_dst, tbl_srs=tbl_srs, join_cond=join_cond, update_cond=update_cond,
                                   update_part=update_part, insrt=insrt, insrt2=insrt2)
        else:  # if all columns are in PK 
            stm = MERGE_STM_WITHOUT_UPDATE.format(tbl_dst=tbl_dst, tbl_srs=tbl_srs, join_cond=join_cond,  insrt=insrt, insrt2=insrt2)

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
  
    def create_pull_sp(self, entity_name, entity_name2=None, src_views_ent=None, create_or_alter=True):
        entity_name2 = entity_name2 or nc.default_rename(entity_name)
        src_views_ent = src_views_ent or entity_name
        _, source_view_name = self.get_view_names(src_views_ent)
        sp_name = nc.pull_sp_name(entity_name=entity_name2)
        dst_tbl = nc.stg_table_name(entity_name)
        ins_stm = self.generate_insert_stm(source_view_name, dst_tbl)
        create_sp_stm = PULL_SP.format(sp_name=sp_name, table_name=dst_tbl, ins_stm=ins_stm, 
                                       or_alter=or_alter(create_or_alter))
        create_sp_stm = apply_sql_formating(create_sp_stm)                              
        return create_sp_stm, sp_name

    def get_table_definition(self, table_name, new_table_name: str = None, drop_existing: bool = True):
        schema_name, table_name = extract_schema_and_table_names(table_name)

        column_query = f"""
        SELECT 
            COLUMN_NAME, 
            DATA_TYPE, 
            IS_NULLABLE, 
            CHARACTER_MAXIMUM_LENGTH, 
            NUMERIC_PRECISION, 
            NUMERIC_SCALE,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{schema_name}'
            ORDER BY ORDINAL_POSITION
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
            ORDER BY IC.key_ordinal,  IX.index_id
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
        if drop_existing:
            script.append(f"drop TABLE if exists [{schema_name}].[{table_name}];" + SQL_GO)
        script.append(f"CREATE TABLE [{schema_name}].[{table_name}] (")
        
        col_defs = []
        for column in columns:
            col_name, data_type, is_nullable, char_length, num_precision, num_scale, column_default = column
            data_type = data_type.upper()
            col_def = f"    [{col_name}] {data_type}"

            # Add length for character types
            if data_type in ('VARCHAR', 'NVARCHAR', 'CHAR', 'NCHAR') and char_length:
                if char_length == -1:
                    char_length = 'MAX'
                col_def += f"({char_length})"
            # Add precision and scale for numeric types
            elif data_type in ('NUMERIC', 'DECIMAL') and num_precision is not None and num_scale is not None:
                col_def += f"({num_precision}, {num_scale})"

            if column_default:
                col_def += f" DEFAULT {column_default}"

            col_def += ' NOT NULL' if is_nullable == 'NO' else ' NULL'
            col_defs.append(col_def)
        script.append(",\n".join(col_defs))

        if primary_keys:
            script.append(f",\n    PRIMARY KEY ({', '.join(primary_keys)})")

        for fk in foreign_keys:
            script.append(f",\n    FOREIGN KEY ([{fk[0]}]) REFERENCES [{fk[1]}]([{fk[2]}])")
        
        script.append("\n);\n")

        index_dict = {}
        for index in indexes:
            index_name, column_name, type_desc, is_unique, fill_factor = index
            if index_name not in index_dict:
                index_dict[index_name] = {
                    'columns': [],
                    'type_desc': type_desc,
                    'is_unique': is_unique,
                    'fill_factor': fill_factor
                }
            index_dict[index_name]['columns'].append(column_name)

        for index_name, index in index_dict.items():
            unique = 'UNIQUE ' if index['is_unique'] else ''
            columns = ", ".join(f"[{col}] ASC" for col in index['columns'])
            script.append(f"CREATE {unique}{index['type_desc']} INDEX [{index_name}] ON [{schema_name}].[{table_name}]({columns})")
            if index['fill_factor']:
                script.append(f" WITH (FILLFACTOR = {index['fill_factor']});")
            else:
                script.append(";")
        # Fix ends here

        return "\n".join(script)

    def create_new_sql_object(self, ot: SQL_OBJECT_TYPE, ents: List[str], src_views_ents: List[str] = [], output_dir: str = None,
                              rppts: List[ReplacementPattern] = None): 
        big_script, new_objects, already_created = '', [], set()
        zz = zip(ents, src_views_ents) if src_views_ents else ents
        for tp in zz:
            entity_name = tp[0] if src_views_ents else tp
            src_views_ent = tp[1] if src_views_ents else None
            new_objects = None
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
                    view_name, view_name2 = self.get_view_names(entity_name)
                    if not view_name:
                        logging.warning(f'View for {entity_name} was not found. Have to skip view cloning')
                        continue
                    new_views = self.deep_clone_view(view_name, view_name2, rppts=rppts)
                    new_objects = [(v[1], v[0], v[4]) for v in new_views]

                    ot_folder = 'Views'
                case SQL_OBJECT_TYPE.PULL_SP:
                    obj_def, obj_name = self.create_pull_sp(entity_name, nc.default_rename(entity_name), src_views_ent)
                    ot_folder = 'StoredProcedures'
                case SQL_OBJECT_TYPE.MERGE_SP:
                    obj_def, obj_name = self.create_merge_sp(entity_name, nc.default_rename(entity_name))                 
                    ot_folder = 'StoredProcedures'
            
            if new_objects is None:  # most of types returns defintions for single object
                new_objects = [(obj_name, obj_def, None)]

            for obj_name, obj_def, db_name in new_objects:
                if obj_name:
                    if obj_name not in already_created:
                        db_name = db_name or self.DB_NAME
                        big_script += f'USE {db_name}' + SQL_GO + obj_def + SQL_GO
                        if output_dir:
                            outo.output_to_file(output_dir, ot_folder, obj_name, obj_def, db_name)
                        already_created.add(obj_name)  # to avoid double creation of child views been refe-ed from many parent views
                else:
                    logging.warning(f'could not create {ot} for {entity_name}. Skipping.')
        return big_script


def parse_db_obj_full_name(obj_name: str) -> List[str]:
    return [x.strip('[]') for x in obj_name.split('.')]


def extract_schema_and_table_names(table_name: str) -> Tuple[str, str]:
    sntn = parse_db_obj_full_name(table_name)
    if len(sntn) == 2:
        schema_name, table_name = sntn[0], sntn[1]
    elif len(sntn) == 1:
        schema_name, table_name = 'dbo', sntn[0]
    return schema_name, table_name


def rename_sql_object(sql_def: str, new_name: str):
    # Regular expression to match creating patterns and capture the original object name
    pattern = r"^(create(?: or alter)?(?:\s+view|\s+procedure|\s+function)?)\s+(\S+\.?\S*)"
    
    def repl(match):
        create_stmt = match.group(1)  # The create or alter statement part
        return f"{create_stmt} {new_name}"

    updated_sql_def = re.sub(pattern, repl, sql_def, flags=re.IGNORECASE | re.MULTILINE)
    return updated_sql_def


def _create_obj_name_for_replacement(obj_name: str, obj_name2: str):
    nnn = parse_db_obj_full_name(obj_name)
    if len(nnn) > 1:
        return f'{nnn[-2]}.{obj_name2}'
    return obj_name2



