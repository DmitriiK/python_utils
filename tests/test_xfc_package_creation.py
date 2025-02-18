import unittest
import pyperclip
from sql.sql_requests import SQL_Communicator
from  sql.xfc_package_creation import create_xfc_ds_table, XFC_Creator, XFC_SourceDB, TransDeliveryStyle
class TestXFCCreation(unittest.TestCase):
    def test_create_source_table(self):
        table_name = 'IDCEquitySecurityToSecurityFeature2_tbl'
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

 



    def test_create_source_table_and_columns(self):
        tbls  = [
            ('IDCEquitySecurityToSecurityFeature2_tbl', 'EqSecurity', TransDeliveryStyle.CHANGE),
            ('IDCEquitySecurity_Security2_tbl', 'EqSecurity', TransDeliveryStyle.CHANGE),
            ('RefData_SecurityGroup_tbl', 'EqSecurity', TransDeliveryStyle.FULL),
            ('RefData_SecuritySubType_tbl', 'EqSecurity', TransDeliveryStyle.FULL),
        ]
        db_id = XFC_SourceDB.DataFeedEngineMI
        sql_script = ''
        with SQL_Communicator() as sqlc:
            xfc_cr = XFC_Creator(sqlc)
            for table_name, pop_gr, tds in tbls:
                sql = create_xfc_ds_table(source_table_name=table_name, 
                                        xfc_database_id=db_id, 
                                        tds=tds, 
                                        population_group=pop_gr) 
                sql_script += '\nGO\n' +sql

                sql = xfc_cr.create_xfc_ds_table_columns(xfc_database_id=XFC_SourceDB.DataFeedEngineMI, source_table_name=table_name) 
                sql_script += '\nGO\n' +sql      
        pyperclip.copy(sql_script) 