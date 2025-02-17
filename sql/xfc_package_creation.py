from enum import Enum
from .sql_requests import SQL_Communicator
from .utils import get_table_schema
from sql.config import DB_NAME_XFC, CONN_STR_XFC

class XFC_SourceDB(Enum):
    DataFeedEngineMI = 7

class TransDeliveryStyle(Enum):
    CHANGE = 'CHANGE'
    FULL = 'FULL'

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


def create_xfc_ds_table_columns(source_table_name: str, source_table_id: int, ):
    def xfc_data_type(col) -> str:
        return f"'{col.data_type} {f'({col.precision})' if 'char' in col.data_type else ''}'"
    
    with SQL_Communicator() as sql_dt:
        cols = sql_dt.get_columns(table_name=source_table_name)
        print(cols)
    col_lst = [f"('{col.column_name}', {xfc_data_type(col)})" 
                for col in cols]

    cols_vals = ', '.join(col_lst)
    sql = cols_vals
    return sql




"""exec sp_executesql N'insert into xfc_SourceColumnProfile 
(columnFormatId, DataType, indexColumnOrder, KeyFlag, popQueryFlag, sourceColumnName, sourceColumnId, sourceTableId) values 
,N'@P0 int,@P1 nvarchar(4000),@P2 smallint,@P3 nvarchar(4000),@P4 bit,@P5 nvarchar(4000),@P6 int,@P7 int',NULL,N'int',1,N'Y',0,N'companyID',13786,7934"""