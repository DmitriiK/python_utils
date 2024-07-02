import pyodbc
import pymssql


conn_str = r"""DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER}; DATABASE={DATABASE}; 
Authentication=ActiveDirectoryPassword;UID=CIQDEV\dmitrii_kalmanovich;PWD=; """

conn_str = (
    r'Driver={ODBC Driver 18 for SQL Server};'
    r'Server=qtdfedbdv01.ciqdev.com\feeds;'
    r'Database=DataFeedngineIndex;'
    r'Trusted_Connection=yes;'
    r'TrustServerCertificate=yes;'
    'Connect Timeout=60'
)


def get_connection():
    print(conn_str)
    conn = pyodbc.connect(conn_str)
    print('connected')

def get_connection2():
    print(conn_str)
    conn = pymssql.connect(
    server=r'QTDFEDBDV01\feeds',
    user=None,
    password=None,
    database='DataFeedngineIndex',
    as_dict=True
)  
    print('connected')

get_connection2()



