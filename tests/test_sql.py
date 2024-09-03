import unittest
import os
from sql.sql_requests import MetaDataRequester
import sql.naming_convention as nc
import sql.output_to as outo

entity_name = 'Symbol_FTTickerSymbol' # 'Symbol_IBESTickerEnhanced'
entity_name2 = nc.default_rename(entity_name)
trg_table = nc.table_name(entity_name2)
stg_tbl = nc.stg_table_name(entity_name)
source_view_name = 'Symbol_FTTicker2Source_vw'


class TestSQL(unittest.TestCase):

    # @unittest.skip('tested already')
    def test_connect(self):
        with MetaDataRequester() as mdr:
            assert not mdr.connection.closed

    def test_get_columns(self):
        with MetaDataRequester() as mdr:
            ret = mdr.get_columns(table_name=trg_table)
            assert ret
            print(ret)

    def test_generate_merge_stm(self):
        with MetaDataRequester() as mdr:
            ret = mdr.generate_merge_stm(tbl_srs=stg_tbl, tbl_dst=trg_table)
            assert ret
            print(ret)

    def test_generate_merge_sp(self):
        with MetaDataRequester() as mdr:
            spdef, spname = mdr.create_merge_sp(entity_name, entity_name2)
            assert spdef, spname
            print(spdef)

            file_path = os.path.join(r'.\output', spname.split('.')[-1] + '.sql')
            outo.output_to_file(file_path, spdef)

    def test_generate_pull_sp(self):
        with MetaDataRequester() as mdr:
            spdef, spname = mdr.create_pull_sp(entity_name, entity_name2, source_view_name=source_view_name)
            assert spdef, spname
            print(spdef)
            file_path = os.path.join(r'.\output', spname.split('.')[-1] + '.sql')
            outo.output_to_file(file_path, spdef)

    def test_generate_create_table_stm(self):
        with MetaDataRequester() as mdr:
            ret = mdr.get_table_script(nc.table_name(entity_name))
            assert ret
            print(ret)


    def test_to_file(self):
        spdef, spname = "create xxx as yyy", 'dbo.xx_sp'
        file_path = os.path.join(r'.\output', spname.split('.')[-1] + '.sql')
        outo.output_to_file(file_path, spdef)
