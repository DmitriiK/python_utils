
SQL_SERVER = 'QTDFEDBDV01.ciqdev.com\\feeds'
DB_NAME = 'DataFeedEngineMI'
CONN_STR = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={SQL_SERVER};'
            f'DATABASE={DB_NAME};'
            f'Trusted_Connection=yes;'
            f'Encrypt=yes;'
            f'TrustServerCertificate=yes;'
        )
