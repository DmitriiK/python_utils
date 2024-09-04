import unittest
import os
from sql.sql_requests import MetaDataRequester
import sql.naming_convention as nc
import sql.output_to as outo

entity_name = 'Symbol_FTTickerSymbol' # 'Symbol_IBESTickerEnhanced'
entity_name2 = nc.default_rename(entity_name)
trg_table = nc.table_name(entity_name2)
stg_tbl = nc.stg_table_name(entity_name)
source_view_name = 'Symbol_FTTicker2Source_vw'
output_dir = r'D:\Code\DatabaseBuild\Instances\DATAFEEDENGINE\Databases\DataFeedEngineMI'

ents = ['Symbol_IBESTickerEnhanced',
        'Symbol_TickerEnhanced',
        'Symbol_CusipEnhanced',
        'Symbol_FTCusip6Symbol',
        'Symbol_FTCusip9Symbol',
        'Symbol_FTISINSymbol',
        'Symbol_ISINEnhanced',
        'Symbol_SECCIKEnhanced',
        'Symbol_SECCIKSymbol',
        'Symbol_SedolEnhanced',
        'Symbol_FTSEDOLSymbol',]

source_views = [
    "Symbol_IBESTickerEnhanced2Source_vw",
    "Symbol_TickerEnhanced2Source_vw",
    "Symbol_CusipEnhanced2Source_vw",
    "Symbol_FTCusip6Symbol2Source_vw",
    "Symbol_FTCusip9Symbol2Source_vw",
    "Symbol_FTISINSymbol2Source_vw",
    "Symbol_ISINEnhanced2Source_vw",    
    "Symbol_SECCIKEnhanced2Source_vw",
    "Symbol_SECCIKSymbol2Source_vw",
    "Symbol_SedolEnhanced2Source_vw",
    "Symbol_FTSEDOLSymbol2Source_vw",
] 


class TestSQL(unittest.TestCase):

    # @unittest.skip('tested already')
    def test_connect(self):
        with MetaDataRequester() as mdr:
            assert not mdr.connection.closed

    def test_get_columns(self):
        with MetaDataRequester() as mdr:
            ret = mdr.get_columns(table_name=trg_table)
            assert ret
            print(ret)

    def test_generate_merge_stm(self):
        with MetaDataRequester() as mdr:
            ret = mdr.generate_merge_stm(tbl_srs=stg_tbl, tbl_dst=trg_table)
            assert ret
            print(ret)

    def test_generate_merge_sp(self):
        with MetaDataRequester() as mdr:
            sps = ''
            for entity_name in ents:
                spdef, spname = mdr.create_merge_sp(entity_name, nc.default_rename(entity_name))
                assert spdef, spname
                sps += spdef +"\nGO\n"

                outo.output_to_file(output_dir, "StoredProcedures", spname, spdef)
            outo.output_to_clipboard(sps)

    def test_generate_pull_sp(self):
        with MetaDataRequester() as mdr:
            sps = ''
            for entity_name, source_view_name in zip(ents, source_views):
                # source_view_name, source_view_name = nc.source_view_name(entity_name)
                spdef, spname = mdr.create_pull_sp(entity_name, nc.default_rename(entity_name), source_view_name)
                assert spdef, spname
                sps += spdef + "\nGO\n"
                outo.output_to_file(output_dir, "StoredProcedures", spname, spdef)
            outo.output_to_clipboard(sps)

    def test_generate_create_table_stm(self):
        with MetaDataRequester() as mdr:
            ret = mdr.get_table_script(nc.table_name(entity_name))
            assert ret
            print(ret)

    def test_to_file(self):
        spdef, object_type, spname = "create table xxx ()", 'Table', 'dbo.xx_tbl'
        file_path = os.path.join(r'.\output')
        outo.output_to_file(file_path, object_type, spname, spdef)
