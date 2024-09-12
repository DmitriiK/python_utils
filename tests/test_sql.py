import unittest
import os
from sql.sql_requests import SQL_Communicator
import sql.naming_convention as nc
import sql.output_to as outo

entity_name = 'Symbol_FTTickerSymbol' # 'Symbol_IBESTickerEnhanced'
entity_name2 = nc.default_rename(entity_name)
trg_table = nc.table_name(entity_name2)
stg_tbl = nc.stg_table_name(entity_name)
source_view_name = 'Symbol_FTTicker2Source_vw'
output_dir = r'D:\Code\DatabaseBuild\Instances\DATAFEEDENGINE\Databases\DataFeedEngineMI'

ents = [  
    'GICS_GICS',
    'Symbol_GVKeySymbol',
    'Symbol_GVKeyEnhanced',
    'Symbol_DandBSymbol',
    'KeyDev_FutureEvent',
    'KeyDev_FutureEventToObjectToEventType',
    'FutureEventMkt_FutureEventMkt',
    'FutureEventMkt_FutureEventMktSplitInfo',
    'FutureEventMkt_FutureEventMktToObjectToEventType'  
    ]

src_views_ents = [    # for views have to create another set of names due to naming inconsistencies
    'GICS_GICS',
    'Symbol_GVKey',
    'Symbol_GVKeyEnhanced',
    'Symbol_DandB',
    'KeyDev_FutureEvent',
    'KeyDev_FutureEventToObjectToEventType',
    'KeyDev_FutureEventMkt',
    'KeyDev_FutureEventMktSplitInfo',
    'KeyDev_FutureEventMktToObjectToEventType'  
    ]   


source_views = [nc.source_view_name(x) for x in src_views_ents] 


class TestSQL(unittest.TestCase):

    # @unittest.skip('tested already')
    def test_connect(self):
        with SQL_Communicator() as mdr:
            assert not mdr.connection.closed

    def test_get_columns(self):
        with SQL_Communicator() as mdr:
            ret = mdr.get_columns(table_name=trg_table)
            assert ret
            print(ret)

    def test_generate_merge_stm(self):
        with SQL_Communicator() as mdr:
            ret = mdr.generate_merge_stm(tbl_srs=stg_tbl, tbl_dst=trg_table)
            assert ret
            print(ret)

    def test_generate_merge_sp(self):
        with SQL_Communicator() as mdr:
            sps = ''
            for entity_name in ents:
                spdef, spname = mdr.create_merge_sp(entity_name, nc.default_rename(entity_name))
                assert spdef, spname
                sps += spdef +"\nGO\n"

                outo.output_to_file(output_dir, "StoredProcedures", spname, spdef)
            outo.output_to_clipboard(sps)

    def test_generate_pull_sp(self):
        with SQL_Communicator() as mdr:
            sps = ''
            for entity_name, source_view_name in zip(ents, source_views):
                # source_view_name, source_view_name = nc.source_view_name(entity_name)
                spdef, spname = mdr.create_pull_sp(entity_name, nc.default_rename(entity_name), source_view_name)
                assert spdef, spname
                sps += spdef + "\nGO\n"
                outo.output_to_file(output_dir, "StoredProcedures", spname, spdef)
            outo.output_to_clipboard(sps)

    def test_generate_create_table_stm(self):
        with SQL_Communicator() as mdr:
            ret = mdr.get_table_script(nc.table_name(entity_name))
            assert ret
            print(ret)

    def test_to_file(self):
        spdef, object_type, spname = "create table xxx ()", 'Table', 'dbo.xx_tbl'
        file_path = os.path.join(r'.\output')
        outo.output_to_file(file_path, object_type, spname, spdef)
