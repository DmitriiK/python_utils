from sql.sql_templates import MERGE_SP
from sql.sql_requests import generate_merge_stm

def create_merge_sp(entity_name):
    merge_stm = generate_merge_stm(entity_name +'_tbl')
    sp_name = '[dbo].[MergeData_{entity_name}_prc]'
    create_sp_stm = MERGE_SP.format(sp_name=sp_name, merge_stm = merge_stm)
    with open(spname + '.sql', rw) as f:
        f.write(create_merge_sp)
