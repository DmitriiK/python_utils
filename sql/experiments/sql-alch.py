
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL





class TableColumn(BaseModel):
    name: str
    type: str
    nullable: bool
    default: str | None = Field(None, description="Default value of the column, if any")
    primary_key: bool


def xx(engine,  table_name: str):

    inspector = inspect(engine)

    # Get columns for a given table
   
    columns = inspector.get_columns(table_name)

    # Convert columns to TableColumn instances
    schema = [
        TableColumn(
            name=col['name'],
            type=str(col['type']),  
            nullable=col['nullable'],
            default=col['default'],
            primary_key=col['primary_key']
        )
        for col in columns
    ]

    # Print schema details
    for column in schema:
        print(column.json(indent=2))


SQL_SERVER = 'QTDFEDBDV01.ciqdev.com\\feeds'
DB_NAME = 'DataFeedEngineMI'
conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={SQL_SERVER};'
            f'DATABASE={DB_NAME};'
            f'Trusted_Connection=yes;'
            f'Encrypt=yes;'
            f'TrustServerCertificate=yes;'
        )

connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn_str})
print(connection_url)

engine = create_engine(connection_url, connect_args={'connect_timeout': 60})

xx(engine=engine, table_name='MATransactionToAdvisor_tbl')