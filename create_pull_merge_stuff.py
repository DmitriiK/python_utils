

import os
import logging
import re
from typing import List
import pyperclip

from file_utils import find_file

sep = """;
GO
"""
root_folder = r'C:\Users\dmitrii_kalmanovich\source\repos\DataFeedEngine\DataFeeEngineMI'
root_folder_tbl = fr'{root_folder}\dbo\Tables'
deploy_script_file_path = 'deploy_scrip.sql'

def get_table_def( table_name) -> str:
    file_name = f'{table_name}.sql'
    ff = find_file(root_folder_tbl, file_name )
    if not ff:
        logging.warn(f'table {table_name} not fould')
    else:
        print(ff)
        with open(ff, 'r', encoding='UTF-8') as tf:
            script=tf.read()
            return script.strip().replace('\ufeff', '')

def create_table_script( table_name, new_table_name, new_schema = None):
    script= get_table_def(table_name)
    script2 = script.replace(table_name, new_table_name)
    if new_schema:
            script2 = script2.replace('[dbo]', new_schema)
            script2 = script2.replace('dbo.', new_schema +'.')
    return script2

def create_view_script( targ_table_name: str, sql_stm: str):
    view_name =f'dbo.DataFeedOut_{targ_table_name}'.replace("_tbl", "_vw")
    script= f"""CREATE VIEW {view_name} as 
    sql_stm"""    
    return script, view_name


def create_pull_sp(sql_definition: str):
       # Regular expression to capture the table name
    table_name_pattern = re.compile(r'CREATE\s+TABLE\s+([^(\s]+)')
    table_name_match = table_name_pattern.search(sql_definition)

    table_name = table_name_match.group(1).split('.')[-1].strip('[]')
    ent_name = table_name.replace('_tbl', '').replace('Transaction', 'Transaction2')
    
    # Regular expression to capture columns between parentheses
    columns_pattern = re.compile(r'\((.*?)\)', re.DOTALL)
    columns_match = columns_pattern.search(sql_definition)
    columns_text = columns_match.group(1).strip()
    cols = [x.strip().split(' ')[0] for x in columns_text.split(',') 
            if not (x.strip().split(' ')[0]).isdigit()] # sorry..
    columns_line = ', '.join(cols)
    sp_name = f'[dbo].[PullData_{ent_name}_prc] '
    trg_tbl = f'[stg].[{table_name}]'
    create_sp_stm = f"""
CREATE   PROCEDURE {sp_name}
AS
BEGIN 
TRUNCATE TABLE {trg_tbl};

INSERT INTO {trg_tbl}
(
    {columns_line}
)
SELECT 
    {columns_line}
FROM [dbo].[DataFeedOut_{ent_name}_vw];
END
"""
    return create_sp_stm, sp_name




def batch_create(create_method, output_dir: str):
    sscr = ''
    ls =  get_table_list()
    for tn in ls:
        scr= get_table_def(tn)
        sp_def, sp_name = create_method(scr)
        sscr += sp_def + sep
        file_name= sp_name.split('.')[-1] #  without schema name
        new_scr_path = f'{output_dir}\\{file_name}.sql'
        with open(new_scr_path, 'w') as wf:
            logging.info(f'writing to {new_scr_path}')
            wf.write(sp_def)
    pyperclip.copy(sscr)

def batch_create_merges():
    batch_create(create_method=create_merge_sp, output_dir=r'output\sps')

def batch_create_pull_sps():
    batch_create(create_method=create_pull_sp, output_dir=r'output\sps')


def create_merge_sp(table_def: str):
    table_pattern = re.compile(r'CREATE TABLE \[dbo\]\.\[(\w+)] \((.+?)\);', re.S)
    index_pattern = re.compile(r'CREATE UNIQUE CLUSTERED INDEX \[.+]\s+ON \[dbo\]\.\[(\w+)]\((.+?)\)', re.S)
    column_pattern = re.compile(r'\s*\[(\w+)]')

    # Extract table and columns definition
    table_match = table_pattern.search(table_def)
    if not table_match:
        raise Exception("Table definition not found.")

    table_name = table_match.group(1)
    columns = table_match.group(2).strip()
    column_matches = column_pattern.findall(columns)

    # Extract index columns
    index_match = index_pattern.search(table_def)
    if not index_match:
        raise Exception("Index definition not found or does not match table name.")

    index_columns = index_match.group(2).split(',')
    index_columns = [col.split()[0].strip('[]') for col in index_columns]

    # Columns for insert and update statements
    insert_columns = ', '.join(f'[{col}]' for col in column_matches)
    values_columns = ', '.join(f'SRC.[{col}]' for col in column_matches)
    update_conditions = ' AND '.join(f'ISNULL(DST.[{col}], \'\') <> ISNULL(SRC.[{col}], \'\')' for col in column_matches if col not in index_columns)
    update_set = ', '.join(f'[{col}] = SRC.[{col}]' for col in column_matches if col not in index_columns)
    on_conditions = ' AND '.join(f'DST.[{col}] = SRC.[{col}]' for col in index_columns)

    trg_table_name = table_name.replace('Transaction', 'Transaction2') 
    sp_name = f'dbo.MergeData_{trg_table_name.replace('_tbl', '')}_prc'

    when_matched_part = f"""WHEN MATCHED
        AND (
            {update_conditions}
        ) THEN 
        UPDATE SET 
        {update_set}""" if update_set else ''

    # Create the MERGE statement
    sp_def = f"""CREATE PROCEDURE {sp_name}    
    AS    
    BEGIN
    MERGE dbo.{trg_table_name} AS DST
    USING stg.{table_name} AS SRC WITH (NOLOCK)
        ON {on_conditions}
    {when_matched_part}
    WHEN NOT MATCHED BY TARGET THEN
        INSERT ({insert_columns})
        VALUES ({values_columns})
    WHEN NOT MATCHED BY SOURCE THEN
        DELETE;
    END;
    """
    return sp_def, sp_name


def get_table_list()-> List[str]:
    ls_file = r'output\globaltables.sql'
    with open(ls_file) as f:
       return [line.strip() for line in f]


def batch_create_view():
    sscr = ''
    ls =  get_table_list()
    ts = parse_PullData_prc()
    for table, stm in ts:
        table_short = table.split('.')[-1]
        if table_short in ls:
            scr, name = create_view_script(table_short, stm)
            sscr += scr + sep
    pyperclip.copy(sscr)


def batch_create_tables():
    sscr = ''
    ls =  get_table_list()
    for tn in ls:
        tnn = tn.replace('MATransaction', 'MATransaction2')       
        # scr =create_table_script( tn, tn, '[stg]')
        scr, obj_name = create_view_script(tnn)
        file_name= obj_name.split('.')[-1] #  without schema name
        new_scr_path = f'output\\stg\\{file_name}.sql'
        with open(new_scr_path, 'w') as wf:
            logging.info(f'writing to {new_scr_path}')
            wf.write(scr)

        sscr +=scr + sep
    pyperclip.copy(sscr)

def parse_PullData_prc():
    file_path = fr'{root_folder}\dbo\Stored Procedures\TransactionMA_PullData_prc.sql'
    with open(file_path, 'r') as f:
        script = f.read()
      # Regex to capture the SELECT INTO statement followed by CREATE INDEX statement
    regex = (r'drop\s+table\s+[a-zA-Z0-9._]+\s+' 
            + r'(SELECT\s.*?\sINTO\s+([a-zA-Z0-9._]+)\s.*?FROM\s+.*?;?)' 
            + r'\s*CREATE\s+UNIQUE')
    pattern = re.compile(regex, re.IGNORECASE | re.DOTALL)

    # Find all matches in the script
    matches = pattern.findall(script)

    for match in matches:
        raw_statement = match[0]
        table_name = match[1]

        # Remove 'INTO <table_name>' part
        sql_statement = re.sub(r'\sINTO\s+' + re.escape(table_name), '', raw_statement, flags=re.IGNORECASE)

        yield (table_name, sql_statement.strip())        

# batch_create_merges()
# batch_create_view()
batch_create_pull_sps()

