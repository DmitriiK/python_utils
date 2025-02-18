from enum import Enum
from .sql_requests import SQL_Communicator
from .utils import get_table_schema
from sql.config import DB_NAME_XFC, CONN_STR_XFC

class XFC_SourceDB(Enum):
    DataFeedEngineMI = 7

class TransDeliveryStyle(Enum):
    CHANGE = 'CHANGE'
    FULL = 'FULL'

class XFC_Creator:
    def __init__(self, sql_dt: SQL_Communicator):
        self.sql_dt=sql_dt

 
    def create_xfc_ds_table_columns(self, source_table_name: str, xfc_database_id: XFC_SourceDB):
        def xfc_data_type(col) -> str:
            return f"'{col.data_type}{f'({col.precision})' if 'char' in col.data_type else ''}'"
        def xfc_data_key_flag(col) -> str:
            return "'y'" if col.is_in_pk else "''"
        
        tbl, sch = get_table_schema(source_table_name)
        cols = self.sql_dt.get_columns(table_name=source_table_name)
        col_lst = [f"('{col.column_name}', {xfc_data_type(col)}, {xfc_data_key_flag(col)})" 
                    for col in cols]
        cols_vals = '\n\t\t,'.join(col_lst)
        sql = f"""
    DECLARE @source_table_id int 
    SELECT top 1  @source_table_id = sourceTableId FROM xfc_SourceTableProfile t 
            WHERE t.sourceTableName ='{tbl}' AND t.sourceTableSchema = '{sch}' AND DataBaseId= {xfc_database_id.value}   
            ORDER BY sourceTableId DESC;
    IF @source_table_id IS NULL  BEGIN
        DECLARE @msg nvarchar(100)
        SELECT @msg = FORMATMESSAGE('Table for %s has not been found in xfc_SourceTableProfile', '{source_table_name}' );
        THROW 50005,  @msg , 1;
    END

    DECLARE @max_id int
    SELECT @max_id = MAX(scp.sourceColumnId) FROM xfc_SourceColumnProfile scp;

    WITH cte_fields AS (
        SELECT *
        FROM (VALUES
        {cols_vals}
        ) AS cte_fields(field_name, data_type, is_in_pk)
    )
    ,new_fls as
    (SELECT * from cte_fields f 
        WHERE f.field_name 	NOT IN (SELECT sourceColumnName  FROM xfc_SourceColumnProfile scp where scp.sourceTableId = @source_table_id)
        )

    ,cte_f_rn AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS rn,
        * FROM new_fls
        )
    --final write
    INSERT INTO xfc_SourceColumnProfile(sourceColumnId, sourceTableId, sourceColumnName, DataType, KeyFlag, indexColumnOrder)
    SELECT 
        rn + @max_id as new_id,
        @source_table_id as source_table_id, 
        field_name, data_type, 
        is_in_pk,
        CASE WHEN is_in_pk = 'y' THEN rn ELSE '' END as index_col_order
    FROM cte_f_rn
    """
        return sql

       
def create_xfc_ds_table(source_table_name: str, xfc_database_id: XFC_SourceDB, tds: TransDeliveryStyle, population_group: str):

    tbl, sch = get_table_schema(source_table_name)

    sql = f"""
    DECLARE @source_table_id int 
    SELECT top 1  @source_table_id = sourceTableId FROM xfc_SourceTableProfile t 
            WHERE t.sourceTableName ='{tbl}' AND t.sourceTableSchema = '{sch}' AND DataBaseId= {xfc_database_id.value}   
            ORDER BY sourceTableId DESC;
    IF @source_table_id IS NULL
        BEGIN
        SELECT @source_table_id = MAX(sourceTableId) + 1 FROM xfc_SourceTableProfile t;
        INSERT INTO xfc_SourceTableProfile (sourceTableId, databaseId, sourceTableName, sourceTableSchema, TransDeliveryStyle, PopGroup) 
            values (@source_table_id, {xfc_database_id.value}, '{tbl}', '{sch}', '{tds.value}', '{population_group}')
        END
        ELSE -- if @source_table_id IS not NULL
            UPDATE stp  SET stp.TransDeliveryStyle =  'FULL', stp.PopGroup='EqSecurity'FROM  xfc_SourceTableProfile stp WHERE sourceTableId=@source_table_id

        """
    return sql
