import unittest
import pyperclip
from  sql.xfc_package_creation import create_xfc_ds_table, create_xfc_ds_table_columns, XFC_SourceDB, TransDeliveryStyle
class TestXFCCreation(unittest.TestCase):
    def test_create_source_table(self):
        table_name = 'IDCEquitySecurity_TradingItem2_tbl'
        sql = create_xfc_ds_table(source_table_name=table_name, 
                                     xfc_database_id=XFC_SourceDB.DataFeedEngineMI, 
                                     tds=TransDeliveryStyle.FULL, 
                                     population_group='EqSecurity')
        
        pyperclip.copy(sql)

    def test_create_source_table_columns(self):
        table_name, tbl_id = 'IDCEquitySecurity_TradingItem2_tbl', 8048
        sql = create_xfc_ds_table_columns(source_table_name=table_name, 
                                          source_table_id=tbl_id)
        
        pyperclip.copy(sql)