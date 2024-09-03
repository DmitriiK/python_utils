import unittest

import pyperclip
from file_parsing.file_utils import clone_table_from_file, clone_tables_from_file

tables_dir = r'C:\Users\dmitrii_kalmanovich\source\repos\DataFeedEngine\DataFeedEngineMI\dbo\Tables'
output_tables_dir = r'D:\Code\DatabaseBuild\Instances\DATAFEEDENGINE\Databases\DataFeedEngineMI'


class TestFileProcessing(unittest.TestCase):

    def test_clone_table_from_file(self):
        entity_name = 'Symbol_FTISINSymbol'
        clone_table_from_file(tables_dir, entity_name, output_tables_dir)

    def test_clone_tables_from_files(self):
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

        ss = clone_tables_from_file(tables_dir, ents, output_tables_dir)
        pyperclip.copy(ss)