import unittest
from  sql.xfc_package_creation import create_xfc_data_source, XFC_SourceDB, TransDeliveryStyle
class TestXFCCreation(unittest.TestCase):
    def test_create_source_table(self):
        table_name = 'IDCEquitySecurity_TradingItem2_tbl'
        create_xfc_data_source(source_table_name=table_name, xfc_database_id=XFC_SourceDB.DataFeedEngineMI, tds=TransDeliveryStyle.FULL)
