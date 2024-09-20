import unittest
import os

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
                outo.output_to_file(output_dir, "StoredProcedures", spname, spdef)
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
            ret = mdr.clone_view(entity_name)
            assert ret
            print(ret)
            pyperclip.copy(ret[0])


    def test_to_file(self):
        spdef, object_type, spname = "create table xxx ()", 'Table', 'dbo.xx_tbl'
        file_path = os.path.join(r'.\output')
        outo.output_to_file(file_path, object_type, spname, spdef)
