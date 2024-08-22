import unittest
from sql.sql_requests import create_connection, get_columns, generate_merge_stm

target_table = 'MATransaction2ToAdvisor_tbl'
source_table = 'stg.MATransactionToAdvisor_tbl'


class TestSQL(unittest.TestCase):


    # @unittest.skip('tested already')
    def test_connect(self):
        conn = create_connection()
        assert (conn)

    def test_get_columns(self):
        ret = get_columns(table_name=target_table)
        assert ret
        print(ret)

    def test_generate_merge_stm(self):
        ret = generate_merge_stm(tbl_srs=source_table, tbl_dst=target_table, )


