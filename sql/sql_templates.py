# Query to get column names and PK status
GET_COLUMNS = """
  SELECT
        c.name  AS column_name,
        t.name AS data_type,
        c.max_length,
        c.precision,
        c.scale,
        c.is_nullable,
        c.is_identity,
        CAST(ISNULL(idc.seed_value, 0) as INT) AS seed_value,
        CAST(ISNULL(idc.increment_value, 0) as INT) AS increment_value,
        ISNULL(dc.definition, '') AS default_constr,
        ISNULL(cc.definition, '') AS check_constr,
       CASE WHEN pki.index_id IS NOT NULL THEN 1 ELSE 0 END AS is_pk,
	   pki.key_ordinal as pk_ordinal
    FROM
        sys.columns c
    JOIN
        sys.types t ON c.user_type_id = t.user_type_id
    LEFT JOIN
        sys.identity_columns idc ON c.object_id = idc.object_id AND c.column_id = idc.column_id
    LEFT JOIN
        sys.default_constraints dc ON c.default_object_id = dc.object_id
    OUTER APPLY (SELECT TOP 1 cc.* FROM   sys.check_constraints cc WHERE c.object_id = cc.parent_object_id AND c.column_id = cc.parent_column_id) cc
    OUTER APPLY (SELECT TOP 1 i.index_id, ic.key_ordinal FROM sys.index_columns ic 
				 JOIN  sys.indexes i 
                    ON ic.object_id = i.object_id AND ic.index_id = i.index_id AND (i.is_primary_key = 1 OR  i.type=1)
				 WHERE c.object_id = ic.object_id AND c.column_id = ic.column_id) pki
    WHERE c.object_id = OBJECT_ID('{table_name}')
    ORDER BY c.column_id
"""

GET_DEPENDENCIES = """
--note - for cross DB references referenced_id will be null
SELECT referenced_id, ob.type_desc,
referenced_entity_name,	referenced_schema_name,	
referenced_database_name, referenced_server_name		
FROM sys.sql_expression_dependencies dep
LEFT JOIN {db_name}sys.objects ob 
    on ob.object_id=dep.referenced_id
WHERE referencing_id = OBJECT_ID(?)
AND referenced_class_desc = 'OBJECT_OR_COLUMN'   
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

MERGE_STM_WITHOUT_UPDATE = """ MERGE {tbl_dst} AS DST
            USING   {tbl_srs} as SRC WITH (NOLOCK)
                ON {join_cond}
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

PULL_SP = """CREATE  {or_alter}  PROCEDURE {sp_name}
AS
BEGIN
    TRUNCATE TABLE  {table_name}
    {ins_stm}; 
END
"""


def or_alter(alter_mi: bool):
    return 'OR ALTER ' if alter_mi else ''

