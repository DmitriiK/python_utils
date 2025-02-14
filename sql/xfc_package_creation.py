from enum import Enum
from .sql_requests import SQL_Communicator
from .utils import get_table_schema
from sql.config import DB_NAME_XFC, CONN_STR_XFC

class XFC_SourceDB(Enum):
    DataFeedEngineMI = 7

class TransDeliveryStyle(Enum):
    CHANGE = 'CHANGE'
    FULL = 'FULL'

def create_xfc_data_source(source_table_name: str, xfc_database_id: XFC_SourceDB, tds: TransDeliveryStyle):
    with SQL_Communicator() as sql_dt:
        cols = sql_dt.get_columns(table_name=source_table_name)
        print(cols)

    
    with SQL_Communicator(db_name=DB_NAME_XFC, conn_str=CONN_STR_XFC) as sql_xfc:
        tbl, sch = get_table_schema(source_table_name)
        sql = """SELECT top 1 sourceTableId FROM xfc_SourceTableProfile t 
                WHERE t.sourceTableName = ? AND t.sourceTableSchema = ? AND DataBaseId= ?
                ORDER BY sourceTableId DESC"""
        tbl_id = sql_xfc.run_select(sql, True, tbl, sch, xfc_database_id.value)
        if not tbl_id:
            sql = 'SELECT MAX(sourceTableId) FROM xfc_SourceTableProfile t'
            tbl_id = sql_xfc.run_select(sql, True)

        print(tbl_id)


"""
insert into xfc_SourceTableProfile (PopGroup, sourceTableName, sourceTableSchema, TransDeliveryStyle, databaseId, sourceTableId) 
values (@P0, @P1, @P2, @P3, @P4, @P5)',
N'@P0 nvarchar(4000),@P1 nvarchar(4000),@P2 nvarchar(4000),@P3 nvarchar(4000),@P4 int,@P5 int',N'GICS',N'GICS_GICS2_tbl',N'dbo',N'CHANGE',7,7934
"""