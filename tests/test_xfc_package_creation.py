import unittest
import pyperclip
from sql.sql_requests import SQL_Communicator
from  sql.xfc_package_creation import create_xfc_ds_table, XFC_Creator, XFC_SourceDB, TransDeliveryStyle
class TestXFCCreation(unittest.TestCase):
    def test_create_source_table(self):
        table_name = 'IDCEquitySecurity_TradingItem2_tbl'
        sql = create_xfc_ds_table(source_table_name=table_name, 
                                     xfc_database_id=XFC_SourceDB.DataFeedEngineMI, 
                                     tds=TransDeliveryStyle.FULL, 
                                     population_group='EqSecurity')
        
        pyperclip.copy(sql)

    def test_create_source_table_columns(self):
        table_name ='IDCEquitySecurity_TradingItem2_tbl'
        with SQL_Communicator() as sqlc:
            xfc_cr = XFC_Creator(sqlc)
            sql = xfc_cr.create_xfc_ds_table_columns(xfc_database_id=XFC_SourceDB.DataFeedEngineMI, source_table_name=table_name)       
            pyperclip.copy(sql)