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
    return f'dbo.{entity_name}_vw'


# renaming patterns for making of clones of some specific tables
def trans_ft_rename(x):
    return x.replace('Transaction', 'Transaction2')


def default_rename(x):
    return x + '2'