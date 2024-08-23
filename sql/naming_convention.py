def table_name(entity_name):
    return f'dbo.{entity_name}_tbl'


def stg_table_name(entity_name):
    return f'stg.{entity_name}_tbl'


def merge_sp_name(entity_name):
    return f'[dbo].[MergeData_{entity_name}_prc]'


# renaming patterns for making of clones of some specific tables
def trans_ft_rename(x):
    return x.replace('Transaction', 'Transaction2')


def default_rename(x):
    return x + '_2'