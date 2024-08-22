import pyodbc
from typing import List
import logging
from collections import namedtuple
from sql.sql_config import SQL_SERVER, DB_NAME


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



def get_columns(table_name: str, schema_name: str = 'dbo') -> List[ColumnInfo]:
    conn = create_connection()
    cursor = conn.cursor()

    # Query to get column names and PK status
    query = f"""
    SELECT
        c.name AS ColumnName,
        CASE
            WHEN i.index_id IS NOT NULL THEN 1
            ELSE 0
        END AS IsPK
    FROM
        sys.columns c
    LEFT JOIN
        sys.index_columns ic ON c.object_id = ic.object_id AND c.column_id = ic.column_id
    LEFT JOIN
        sys.indexes i ON ic.object_id = i.object_id AND ic.index_id = i.index_id AND (i.is_primary_key = 1 OR  i.type=1)
    WHERE
        c.object_id = OBJECT_ID('{schema_name}.{table_name}')
    """

    # Execute the query
    cursor.execute(query)
    columns = [ColumnInfo(row.ColumnName, bool(row.IsPK)) for row in cursor.fetchall()]

    # Close the connection
    cursor.close()
    conn.close()

    return columns


def generate_merge_stm(tbl_srs: str, tbl_dst: str):
    cols = get_columns(table_name=tbl_dst)
    insrt = ', '.join([x.column_name for x in cols])
    insrt2 = ', '.join([f'SRC.{x.column_name}' for x in cols])

    join_cond = ' AND '.join([f'DST.{x.column_name} = SRC.{x.column_name}' for x in cols if x.is_in_pk])
    non_pk_cols = [x.column_name for x in cols if not x.is_in_pk]
    update_part = ',\n'.join([f'{x} = SRC.{x}' for x in non_pk_cols])
    update_cond = ' AND '.join([f"ISNULL(DST.{x}, 0) <> ISNULL(SRC.{x}, 0) " for x in non_pk_cols])

    stm = f""" MERGE {tbl_dst} AS DST
            USING   {tbl_srs} as SRC WITH (NOLOCK)
                ON {join_cond}
            WHEN MATCHED
                AND (
                    {update_cond}
                ) THEN
                UPDATE SET
                   {update_part}
            WHEN NOT MATCHED BY TARGET THEN
                INSERT ({insrt})
                VALUES ({insrt2})
            WHEN NOT MATCHED BY SOURCE THEN
                DELETE
            ;"""
    print(stm)
    return stm