import unittest

import pyperclip
from file_parsing.file_utils import clone_table_from_file, clone_tables_from_file, clone_view_from_file, clone_views_from_file
import sql.naming_convention as nc
tables_dir = r'C:\Users\dmitrii_kalmanovich\source\repos\DataFeedEngine\DataFeedEngineMI2\dbo'
output_dir = r'D:\Code\DatabaseBuild\Instances\DATAFEEDENGINE\Databases\DataFeedEngineMI'
ents = [    

    'GICS_GICS',
    'Symbol_GVKeySymbol',
    'Symbol_GVKeyEnhanced',
    'Symbol_DandBSymbol',
    'KeyDev_FutureEvent',
    'KeyDev_FutureEventToObjectToEventType',
    'FutureEventMkt_FutureEventMkt',
    'FutureEventMkt_FutureEventMktSplitInfo',
    'FutureEventMkt_FutureEventMktToObjectToEventType'  
    ]

src_views_ents = [    # for views have to create another set of names due to naming inconsistencies
    'GICS_GICS',
    'Symbol_GVKey',
    'Symbol_GVKeyEnhanced',
    'Symbol_DandB',
    'KeyDev_FutureEvent',
    'KeyDev_FutureEventToObjectToEventType',
    'KeyDev_FutureEventMkt',
    'KeyDev_FutureEventMktSplitInfo',
    'KeyDev_FutureEventMktToObjectToEventType'  
    ]   


class TestFileProcessing(unittest.TestCase):

    def test_clone_table_from_file(self):
        entity_name = 'Symbol_FTISINSymbol'
        clone_table_from_file(tables_dir, entity_name, output_dir)

    def test_clone_view_from_files(self):
        entity_name = 'Symbol_FTCusip6Symbol'
        clone_view_from_file(tables_dir, entity_name, output_dir)

    def test_clone_tables_from_files(self):
        ss = clone_tables_from_file(tables_dir, ents, output_dir)
        pyperclip.copy(ss)

    def test_clone_views_from_files(self):
        ss = clone_views_from_file(tables_dir, src_views_ents, output_dir, nc_view_name=nc.source_view_name)
        pyperclip.copy(ss)



