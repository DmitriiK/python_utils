import unittest
import os
from sql.sql_requests import MetaDataRequester
import sql.naming_convention as nc
import sql.output_to as outo

entity_name = 'MATransactionToAdvisor'
entity_name2 = nc.trans_ft_rename(entity_name)
trg_table = nc.table_name(entity_name2)
stg_tbl = nc.stg_table_name(entity_name)


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



    def test_to_file(self):
        spdef, spname = "create xxx as yyy", 'dbo.xx_sp'
        file_path = os.path.join(r'.\output', spname.split('.')[-1] + '.sql')
        outo.output_to_file(file_path, spdef)
