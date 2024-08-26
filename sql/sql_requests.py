import pyodbc
from typing import List
import logging
from collections import namedtuple

from sql.config import SQL_SERVER, DB_NAME
from sql.sql_templates import GET_COLUMNS, MERGE_STM


ColumnInfo = namedtuple('ColumnInfo', ['column_name', 'is_in_pk'])


class MetaDataRequester:
    def __enter__(self):
        self.conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={SQL_SERVER};'
            f'DATABASE={DB_NAME};'
            f'Trusted_Connection=yes;'
            f'Encrypt=yes;'
            f'TrustServerCertificate=yes;'
        )
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

        # Query to get column names and PK status
        query = GET_COLUMNS.format(table_name=table_name)
        # Execute the query
        cursor.execute(query)
        columns = [ColumnInfo(row.ColumnName, bool(row.IsPK)) for row in cursor.fetchall()]
        cursor.close()

        if not columns:
            raise Exception(f'looks like table {table_name} has not been created yet')

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

    def get_table_script(self, table_name, schema='dbo'):
        cursor = self.connection.cursor()
        
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
