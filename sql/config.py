
SQL_SERVER = 'QTDFEDBDV01.ciqdev.com\\feeds'
DB_NAME = 'DataFeedEngineMI'

SQL_SERVER_XFC = 'QTDFEDBDV05.ciqdev.com\\feeds7'
DB_NAME_XFC = 'DataFeedEngineXFC'

__CONN_STR_TMPL = (
            'DRIVER={{ODBC Driver 17 for SQL Server}};'
            'SERVER={SQL_SERVER};'
            'DATABASE={DB_NAME};'
            'Trusted_Connection=yes;'
            'Encrypt=yes;'
            'TrustServerCertificate=yes;'
        )

CONN_STR = __CONN_STR_TMPL.format(SQL_SERVER=SQL_SERVER, DB_NAME = DB_NAME)
CONN_STR_XFC = __CONN_STR_TMPL.format(SQL_SERVER=SQL_SERVER_XFC, DB_NAME = DB_NAME_XFC)




