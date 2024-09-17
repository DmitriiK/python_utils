from typing import List
import re

import sqlparse
from configs.lauch_config import ReplacementPattern


def apply_mappings(input_str: str, rps: List[ReplacementPattern]):
    for rp in rps:
        pattern = re.compile(rp.re_replace_this, re.IGNORECASE)
        input_str = re.sub(pattern, rp.replace_to, input_str)
    return input_str


def apply_sql_formating(script: str):
    return sqlparse.format(script, reindent=True, keyword_case='upper')
