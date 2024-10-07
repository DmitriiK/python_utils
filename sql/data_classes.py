from dataclasses import dataclass
from enum import Enum


class DB_Object_Type(Enum):
    USER_TABLE = 'USER_TABLE'
    VIEW = 'VIEW'
    SQL_STORED_PROCEDURE = 'SQL_STORED_PROCEDURE'
    SQL_SCALAR_FUNCTION = 'SQL_SCALAR_FUNCTION'  
    SQL_INLINE_TABLE_VALUED_FUNCTION = 'SQL_INLINE_TABLE_VALUED_FUNCTION'
    CLR_STORED_PROCEDURE = 'CLR_STORED_PROCEDURE'


@dataclass
class SQL_Object:
    object_id: int
    name: str
    type: DB_Object_Type
    schema: str = 'dbo'
    db_name: str = None
    server_name: str = None

    @property
    def full_name(self):
        nnn = f'{self.schema or 'dbo'}.{self.name}'
        if self.db_name:
            nnn = f'{self.db_name}.{nnn}'
            if self.server_name:
                nnn = f'{self.server_name}.{nnn}'
        return nnn

    
