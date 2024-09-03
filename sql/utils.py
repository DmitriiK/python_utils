def get_table_schema_db(object_name: str):
    ss = [x.strip('[]') for x in object_name.split('.')]
    match len(ss):
        case 1:
            return (ss[0], 'dbo', None)  # table name only means dbo by default
        case 2:
            return (ss[1], ss[0], None)  # table name only means dbo by default
        case 3:
            return (ss[2], ss[1], ss[0])  # table name only means dbo by default
        case _:
            raise ValueError('incorrect name of object')