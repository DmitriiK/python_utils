

import os
import logging
import re
from typing import List
import pyperclip

from file_utils import find_file
root_folder_tbl = r'C:\Users\dmitrii_kalmanovich\source\repos\DataFeedEngine\DataFeeEngineMI\dbo\Tables'
deploy_script_file_path = 'deploy_scrip.sql'

def create_table_script( table_name, new_table_name, new_schema = None):
    file_name = f'{table_name}.sql'
    ff = find_file(root_folder_tbl, file_name )
    if not ff:
        logging.warn(f'table {table_name} not fould')
    else:
        print(ff)
        with open(ff, 'r', encoding='UTF-8') as tf:
            script=tf.read()
            script2 = script.replace(table_name, new_table_name)
            if new_schema:
                 script2 = script2.replace('[dbo]', new_schema)
                 script2 = script2.replace('dbo.', new_schema +'.')

            return script2.strip().replace('\ufeff', '')

def create_merge_sp(table_def: str):

    # Regex patterns to extract information
    table_pattern = re.compile(r'CREATE TABLE \[dbo\]\.\[(\w+)] \((.+?)\);', re.S)
    index_pattern = re.compile(r'CREATE UNIQUE CLUSTERED INDEX \[.+]\s+ON \[dbo\]\.\[\1]\((.+?)\)', re.S)
    column_pattern = re.compile(r'\s*\[(\w+)]')

    # Extract table and columns definition
    table_match = table_pattern.search(table_def)
    table_name = table_match.group(1)
    columns = table_match.group(2).strip()
    column_matches = column_pattern.findall(columns)

    # Extract index columns
    index_match = index_pattern.search(table_def)
    index_columns = index_match.group(1).split(',')
    index_columns = [col.split()[0].strip('[]') for col in index_columns]

    # Columns for insert and update statements
    insert_columns = ', '.join(f'[{col}]' for col in column_matches)
    values_columns = ', '.join(f'SRC.[{col}]' for col in column_matches)
    update_conditions = ' AND '.join(f'ISNULL(DST.[{col}], \'\') <> ISNULL(SRC.[{col}], \'\')' for col in column_matches if col not in index_columns)
    update_set = ', '.join(f'[{col}] = SRC.[{col}]' for col in column_matches if col not in index_columns)
    on_conditions = ' AND '.join(f'DST.[{col}] = SRC.[{col}]' for col in index_columns)

    # Create the MERGE statement
    merge_statement = f"""
    MERGE dbo.{table_name} AS DST
    USING stg.{table_name} AS SRC WITH (NOLOCK)
    ON {on_conditions}
    WHEN MATCHED
        AND (
            {update_conditions}
        ) THEN 
        UPDATE SET 
        {update_set}
    WHEN NOT MATCHED BY TARGET THEN
        INSERT ({insert_columns})
        VALUES ({values_columns})
    WHEN NOT MATCHED BY SOURCE THEN
        DELETE;
    """

    return merge_statement


def get_table_list()-> List[str]:
    ls_file = r'output\globaltables.sql'
    with open(ls_file) as f:
       return [line.strip() for line in f]


def batch_create_tables():
    sscr = ''
    sep = """;
    GO
    """
    ls =  get_table_list()
    for tn in ls:
        tnn = tn.replace('Transaction', 'Transaction2')       
        scr =create_table_script( tn, tn, '[stg]')
        new_scr_path = f'output\\stg\\{tn}.sql'
        with open(new_scr_path, 'w') as wf:
            logging.info(f'writing to {new_scr_path}')
            wf.write(scr)

        sscr +=scr + sep
    pyperclip.copy(sscr)

