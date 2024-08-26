import pyodbc
from typing import List
import logging
from collections import namedtuple

from sql.config import SQL_SERVER, DB_NAME
from sql.sql_templates import GET_COLUMNS, MERGE_STM


ColumnInfo = namedtuple('ColumnInfo', ['column_name', 'is_in_pk'])


# Define the server and database parameters
def create_connection():
    connection_string = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={SQL_SERVER};'
        f'DATABASE={DB_NAME};'
        f'Trusted_Connection=yes;'
        f'Encrypt=yes;'
        f'TrustServerCertificate=yes;'
    )
    logging.info(connection_string)
    print('connecting...')
    connection = pyodbc.connect(connection_string, timeout=60)
    print("Connection successful!")
    return connection


def get_columns(table_name: str) -> List[ColumnInfo]:
    conn = create_connection()
    cursor = conn.cursor()

    # Query to get column names and PK status
    query = GET_COLUMNS.format(table_name=table_name)
    # Execute the query
    cursor.execute(query)
    columns = [ColumnInfo(row.ColumnName, bool(row.IsPK)) for row in cursor.fetchall()]

    # Close the connection
    cursor.close()
    conn.close()
    if not columns:
        raise Exception(f'looks like table {table_name} has not been created yet')

    return columns


def generate_merge_stm(tbl_srs: str, tbl_dst: str) -> str:
    cols = get_columns(table_name=tbl_dst)
    insrt = ', '.join([x.column_name for x in cols])
    insrt2 = ', '.join([f'SRC.{x.column_name}' for x in cols])

    join_cond = ' AND '.join([f'DST.{x.column_name} = SRC.{x.column_name}' for x in cols if x.is_in_pk])
    non_pk_cols = [x.column_name for x in cols if not x.is_in_pk]
    update_part = ',\n'.join([f'{x} = SRC.{x}' for x in non_pk_cols])
    update_cond = ' AND '.join([f"ISNULL(DST.{x}, 0) <> ISNULL(SRC.{x}, 0) " for x in non_pk_cols])
    stm = MERGE_STM.format(tbl_dst=tbl_dst, tbl_srs=tbl_srs, join_cond=join_cond, update_cond=update_cond,
                           update_part=update_part, insrt=insrt, insrt2=insrt2)
    return stm


def generate_insert_stm(view_srs: str, tbl_dst: str) -> str:
    cols = get_columns(table_name=tbl_dst)
    cols_str = ','.join([x.column_name for x in cols])

    return f"""INSERT INTO {tbl_dst} ({cols_str})
    SELECT {cols_str} FROM {view_srs}"""
