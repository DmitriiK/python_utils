import re

suffix_view_name = '_vw'
suffix_src_view_name = 'Source' + suffix_view_name
suffix_tbl = '_tbl'


def remove_second_occurrence(text, substring):
    # Find all occurrences of the substring (case-insensitive)
    matches = list(re.finditer(re.escape(substring), text, re.IGNORECASE))
    if len(matches) < 2:
        return text  # Return the original text if less than two occurrences
    # Get the start and end positions of the second occurrence
    start, end = matches[1].span()    
    # Remove the second occurrence
    new_text = text[:start] + text[end:]
    return new_text


def table_name(entity_name):
    return f'dbo.{entity_name}_tbl'


def stg_table_name(entity_name):
    return f'stg.{entity_name}_tbl'


def dst_table_name(entity_name):
    return f'dbo.{entity_name}_tbl'


def merge_sp_name(entity_name):
    return f'dbo.MergeData_{entity_name}_prc'


def pull_sp_name(entity_name):
    return f'dbo.PullData_{entity_name}_prc'


def source_view_name(entity_name):
    return f'dbo.{entity_name}{suffix_src_view_name}'


def view_name(entity_name):
    return f'dbo.{entity_name}{suffix_view_name}'


def entity_name_from_view_name(view_name):
    view_name = view_name.split('.')[-1].strip('[]')
    found = False
    for sf in suffix_src_view_name, suffix_view_name, suffix_tbl:
        if view_name.lower().endswith(sf.lower()):
            entity_name = view_name[:-len(sf)]
            found = True
            break
    if not found:
        raise ValueError(f'view name {view_name} does not meet naming convention')
    if sf == suffix_tbl:  # shit happens, and in such cases we will rename it using "vw" convention
        sf = suffix_view_name
    return entity_name, sf


def fix_shit(entity_name):
    return remove_second_occurrence(entity_name, 'Symbol')


# renaming patterns for making of clones of some specific tables
def trans_ft_rename(x):
    return x.replace('Transaction', 'Transaction2')


def default_rename(x):
    return x + '2'
