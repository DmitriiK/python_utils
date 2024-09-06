from typing import List, Tuple
import re

import sqlparse

src_view_mapp = [(r'\[?(DatafeedEngine\]?|DatafeedEngineCache)\.\[?dbo\]?\.\[?Universe_DailyCompany_tbl\]?', 
                   'dbo.Universe_Company2_tbl'),
                 (r'\bCIQDataSnapshot\.',
                    'CIQData.')
                ]


def apply_mappings(input_str: str, mappings: List[Tuple[str, str]]):
    for str_pattern, repl in mappings:
        pattern = re.compile(str_pattern, re.IGNORECASE)
        input_str = re.sub(pattern, repl, input_str)
    return input_str


def apply_or_alter(script: str):
    cral = "CREATE or ALTER "
    if not re.search(cral, script, re.IGNORECASE):
        pattern = re.compile(r'\bCREATE ', re.IGNORECASE)
        return re.sub(pattern, cral, script)
    return script


def apply_sql_formating(script: str):
    return sqlparse.format(script, reindent=True, keyword_case='upper')


def test_mapping():
    inp = """
    FROM CIQDataSnapshot.dbo.XXX
    JOIN DatafeedEngine.dbo.[Universe_DailyCompany_tbl] on
    """
    replaced = apply_mappings(inp, src_view_mapp)
    print(replaced)


# test_mapping()