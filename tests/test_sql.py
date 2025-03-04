import unittest
import os   
from pprint import pprint
import pyperclip

from sql.sql_requests import SQL_Communicator
import sql.naming_convention as nc
import sql.output_to as outo
from configs.lauch_config import load_launch_config

entity_name = 'Symbol_FTTickerSymbol' # 'Symbol_IBESTickerEnhanced'
entity_name2 = nc.default_rename(entity_name)
trg_table = nc.table_name(entity_name2)
stg_tbl = nc.stg_table_name(entity_name)
source_view_name = 'Symbol_FTTicker2Source_vw'


launch_config_file = r'configs\launch_configs\launch_config.yml'
lc = load_launch_config(launch_config_file)
output_dir = lc.output_folder

ents = lc.entities
src_views_ents = lc.src_views_ents

source_views = [nc.source_view_name(nc.default_rename(x)) for x in src_views_ents] 


class TestSQL(unittest.TestCase):

    # @unittest.skip('tested already')
    def test_connect(self):
        with SQL_Communicator() as mdr:
            assert not mdr.connection.closed

    def test_get_columns(self):
        with SQL_Communicator() as mdr:
            ret = mdr.get_columns(table_name=trg_table)
            assert ret
            print(ret)

    def test_generate_merge_stm(self):
        with SQL_Communicator() as mdr:
            ret = mdr.generate_merge_stm(tbl_srs=stg_tbl, tbl_dst=trg_table)
            assert ret
            print(ret)

    def test_generate_merge_sp(self):
        with SQL_Communicator() as mdr:
            sps = ''
            for entity_name in ents:
                spdef, spname = mdr.create_merge_sp(entity_name, nc.default_rename(entity_name))
                assert spdef, spname
                sps += spdef +"\nGO\n"

                outo.output_to_file(output_dir, "StoredProcedures", spname, spdef)
            outo.output_to_clipboard(sps)

    def test_generate_pull_sp(self):
        with SQL_Communicator() as mdr:
            sps = ''
            for entity_name, source_view_name in zip(ents, source_views):
                # source_view_name, source_view_name = nc.source_view_name(entity_name)
                spdef, spname = mdr.create_pull_sp(entity_name, nc.default_rename(entity_name), source_view_name)
                assert spdef, spname
                sps += spdef + "\nGO\n"
                outo.output_to_file(output_dir, "StoredProcedures", spname, spdef, mdr.DB_NAME)
            outo.output_to_clipboard(sps)

    def test_create_table_stm(self):
        with SQL_Communicator() as mdr:
            table_name = nc.table_name(entity_name)
            new_table_name = nc.stg_table_name(entity_name)
            ret = mdr.get_table_definition(table_name, new_table_name)
            assert ret
            print(ret)

    def test_clone_view(self):
        entity_name = 'KeyDev_FutureEvent'

        with SQL_Communicator() as mdr:
            view_name, view_name2 = mdr.get_view_names(entity_name, nc.source_view_name)
            ret = mdr.clone_view(view_name, view_name2, lc.code_replacements)
            assert ret
            print(ret)
            pyperclip.copy(ret[0])

    def test_deep_clone_view(self):
        entity_name = 'Professional_Person'
        with SQL_Communicator() as mdr:
            view_name, view_name2 = mdr.get_view_names(entity_name, nc.source_view_name)
            ret = mdr.deep_clone_view(view_name, view_name2, lc.code_replacements)
            assert len(ret) > 1
            for dd in ret[: -1]:
                assert dd[1] in ret[-1][0]  # new name of cloned child view should be in the definition of parent view
            print(ret)

    def test_dependencies(self):
        from sql.data_classes import DB_Object_Type
        entity_name = '[KeyDev_KeyDevPlusSource_vw]'
        filter = DB_Object_Type.VIEW
        with SQL_Communicator() as mdr:
            ret = mdr.get_object_dependencies(entity_name, is_recursive=True, db_object_type=filter)
        assert ret
        pprint(ret)

    def test_table_size(self):
        tbl = 'stg.Professional_Compensation_tbl'
        with SQL_Communicator() as sc:
            rows_count, table_size = sc.get_table_size(tbl)
            print(f'rows {rows_count}, stage table size: {table_size}')

    def test_to_file(self):
        spdef, object_type, spname = "create table xxx ()", 'Table', 'dbo.xx_tbl'
        file_path = os.path.join(r'.\output')
        outo.output_to_file(file_path, object_type, spname, spdef)

