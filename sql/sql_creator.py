import sql.sql_templates as tmpl
import sql.naming_convention as nc
from sql.sql_requests import generate_merge_stm


def create_merge_sp(entity_name, entity_name2=None, create_or_alter=True):
    entity_name2 = entity_name2 or nc.default_rename(entity_name)
    sp_name = nc.merge_sp_name(entity_name=entity_name2)
    dst_tbl = nc.table_name(entity_name2)
    src_tbl = nc.stg_table_name(entity_name)
    merge_stm = generate_merge_stm(dst_tbl, src_tbl)
    create_sp_stm = tmpl.MERGE_SP.format(sp_name=sp_name, merge_stm=merge_stm, or_alter=tmpl.or_alter(create_or_alter))
    return create_sp_stm, sp_name
   
