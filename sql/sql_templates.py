# Query to get column names and PK status
GET_COLUMNS = """
SELECT
    c.name AS ColumnName,
    CASE
        WHEN i.index_id IS NOT NULL THEN 1
        ELSE 0
    END AS IsPK
FROM
    sys.columns c
LEFT JOIN
    sys.index_columns ic ON c.object_id = ic.object_id AND c.column_id = ic.column_id
LEFT JOIN
    sys.indexes i ON ic.object_id = i.object_id AND ic.index_id = i.index_id AND (i.is_primary_key = 1 OR  i.type=1)
WHERE
    c.object_id = OBJECT_ID('{table_name}')
"""

MERGE_STM = """ MERGE {tbl_dst} AS DST
            USING   {tbl_srs} as SRC WITH (NOLOCK)
                ON {join_cond}
            WHEN MATCHED
                AND (
                    {update_cond}
                ) THEN
                UPDATE SET
                   {update_part}
            WHEN NOT MATCHED BY TARGET THEN
                INSERT ({insrt})
                VALUES ({insrt2})
            WHEN NOT MATCHED BY SOURCE THEN
                DELETE
            ;"""


MERGE_SP = """CREATE {or_alter}PROCEDURE {sp_name}
  AS
  BEGIN
      {merge_stm}
  END"""

PULL_SP = """"CREATE  {or_alter}  PROCEDURE {sp_name}
AS
BEGIN
    TRUNCATE TABLE  {table_name}
    {ins_stm};
END
"""


def or_alter(alter_mi: bool):
    return 'OR ALTER ' if alter_mi else ''

