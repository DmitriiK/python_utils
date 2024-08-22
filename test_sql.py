import unittest
from sql.sql_requests import create_connection, get_columns


class TestSQL(unittest.TestCase):

    # @unittest.skip('tested already')
    def test_connect(self):
        conn = create_connection()
        assert (conn)

    def test_get_columns(self):
        ret = get_columns(table_name='CompanyDaily_Company_tbl')
        assert ret
        print(ret)

