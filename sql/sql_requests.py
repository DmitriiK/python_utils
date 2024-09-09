import pyodbc
from typing import List
import logging
from collections import namedtuple

from sql.config import CONN_STR
from sql.sql_templates import GET_COLUMNS, MERGE_STM, MERGE_SP, PULL_SP, or_alter
import sql.naming_convention as nc


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


class SQL_Communicator:
    def __enter__(self):
        self.conn_str = CONN_STR
        logging.info(self.conn_str)
        print('connecting...')
        self.connection = pyodbc.connect(self.conn_str, timeout=60)
        print("Connection successful!")
        return self

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
        return create_sp_stm, sp_name
  
    def create_pull_sp(self, entity_name, entity_name2=None, source_view_name=None, create_or_alter=True):
        entity_name2 = entity_name2 or nc.default_rename(entity_name)
        source_view_name = source_view_name or nc.source_view_name(entity_name)
        sp_name = nc.pull_sp_name(entity_name=entity_name2)
        dst_tbl = nc.stg_table_name(entity_name)
        ins_stm = self.generate_insert_stm(source_view_name, dst_tbl)
        create_sp_stm = PULL_SP.format(sp_name=sp_name, table_name=dst_tbl, ins_stm=ins_stm, 
                                       or_alter=or_alter(create_or_alter))
        return create_sp_stm, sp_name

    def get_table_script(self, table_name):
        cursor = self.connection.cursor()
        ts = table_name.split('.')
        if len(ts) > 1:
            table_name = ts[1].strip('[]')
            schema = ts[0].strip('[]')
        else:
            table_name = ts[0].strip('[]')
            schema = 'dbo'
        # Get the table creation script.
        cursor.execute(f'''
            SELECT c.*
            FROM INFORMATION_SCHEMA.TABLES AS t
            INNER JOIN INFORMATION_SCHEMA.COLUMNS AS c
            ON t.TABLE_SCHEMA = c.TABLE_SCHEMA AND t.TABLE_NAME = c.TABLE_NAME
            WHERE t.TABLE_TYPE = 'BASE TABLE'
            AND t.TABLE_SCHEMA = '{schema}'
            AND t.TABLE_NAME = '{table_name}'
            ORDER BY c.ORDINAL_POSITION
        ''')
        
        columns = cursor.fetchall()
        
        col_definitions = []
        for col in columns:
            col_definition = f"[{col.COLUMN_NAME}] {col.COLUMN_TYPE}"
            if col.IS_NULLABLE == 'NO':
                col_definition += " NOT NULL"
            if col.COLUMN_DEFAULT:
                col_definition += f" DEFAULT {col.COLUMN_DEFAULT}"
            col_definitions.append(col_definition)

        create_script = f"CREATE TABLE [{schema}].[{table_name}] (\n    " + ",\n    ".join(col_definitions) + "\n);\n"

        # Get the primary key constraints
        cursor.execute(f'''
            SELECT column_name
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = '{schema}'
            AND TABLE_NAME = '{table_name}'
            AND CONSTRAINT_NAME LIKE 'PK_%'
        ''')
        
        primary_keys = cursor.fetchall()
        if primary_keys:
            pk_columns = ", ".join(f"[{pk.column_name}]" for pk in primary_keys)
            create_script += f"ALTER TABLE [{schema}].[{table_name}] ADD PRIMARY KEY ({pk_columns});\n"
        
        # Get the indexes
        cursor.execute(f'''
            SELECT i.name AS IndexName, i.is_unique, c.name AS ColumnName
            FROM sys.indexes AS i
            INNER JOIN sys.index_columns AS ic
            ON i.object_id = ic.object_id AND i.index_id = ic.index_id
            INNER JOIN sys.columns AS c
            ON ic.object_id = c.object_id AND ic.column_id = c.column_id
            INNER JOIN sys.tables AS t
            ON t.object_id = i.object_id
            WHERE t.name = '{table_name}'
        ''')
        
        indexes = cursor.fetchall()
        index_definitions = {}
        for index in indexes:
            if index.IndexName not in index_definitions:
                index_type = "UNIQUE INDEX" if index.is_unique else "INDEX"
                index_definitions[index.IndexName] = {
                    "type" : index_type,
                    "columns" : []
                }
            index_definitions[index.IndexName]["columns"].append(index.ColumnName)
        
        for index_name, index_def in index_definitions.items():
            columns = ", ".join(f"[{col}]" for col in index_def["columns"])
            create_script += f"CREATE {index_def['type']} [{index_name}] ON [{schema}].[{table_name}] ({columns});\n"
        
        return create_script
