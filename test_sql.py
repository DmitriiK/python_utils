import unittest
from sql.sql_requests import create_connection, get_columns, generate_merge_stm
import sql.naming_convention as nc
import sql.sql_creator as sqlcr

entity_name = 'MATransactionToAdvisor'
entity_name2 = nc.trans_ft_rename(entity_name)
trg_table = nc.table_name(entity_name2)
stg_tbl = nc.stg_table_name(entity_name)


class TestSQL(unittest.TestCase):

    # @unittest.skip('tested already')
    def test_connect(self):
        conn = create_connection()
        assert (conn)

    def test_get_columns(self):
        ret = get_columns(table_name=trg_table)
        assert ret
        print(ret)

    def test_generate_merge_stm(self):
        ret = generate_merge_stm(tbl_srs=stg_tbl, tbl_dst=trg_table)
        assert ret
        print(ret)

    def test_generate_merge_sp(self):
        ret = sqlcr.create_merge_sp(entity_name, entity_name2)
        assert ret
        print(ret)
