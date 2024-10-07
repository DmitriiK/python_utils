from typing import List
import re

import sqlparse
from configs.lauch_config import ReplacementPattern


def apply_mappings(input_str: str, rps: List[ReplacementPattern]):
    """applying some code replacemements, defined in configs_

    Args:
        input_str (str): _description_
        rps (List[ReplacementPattern]):regex patterns for string replacements

    Returns:
        _type_: same string but after string replacements
    """
    for rp in rps:
        pattern = re.compile(rp.re_replace_this, re.IGNORECASE)
        input_str = re.sub(pattern, rp.replace_to, input_str)
    return input_str


def apply_create_or_alter_view(input_str: str):
    re_replace_this, replace_to = (r'\bCREATE\s+VIEW\s+',
                                   'CREATE or ALTER VIEW ')
    pattern = re.compile(re_replace_this, re.IGNORECASE)
    out_str = re.sub(pattern, replace_to, input_str)
    return out_str


def apply_sql_formating(script: str):
    return sqlparse.format(script, reindent=True, keyword_case='upper')
