import os
import re
from typing import List
import sql.naming_convention as nc


def find_file(root_folder, filename):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    return None


def rename_and_modify_sql_files(folder_path):
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file has a "_stg" prefix (case-insensitive) anywhere in the name
        if '_stg' in filename.lower():
            # Construct the new filename by removing the prefix
            new_filename = re.sub(r'_stg', '', filename, flags=re.IGNORECASE)
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            # Read the contents of the file
            with open(old_file_path, 'r') as file:
                content = file.read()
            
            # Replace all occurrences of "_stg" prefix and schema name
            # Replace all occurrences of "_stg" prefix and schema name
            content = re.sub(r'_stg', '', content, flags=re.IGNORECASE)
            content = re.sub(r'\bdbo\.', 'stg.', content, flags=re.IGNORECASE)
            content = re.sub(r'\[dbo\]\.', 'stg.', content, flags=re.IGNORECASE)
                        
            # Write the modified content to the new file
            with open(new_file_path, 'w') as file:
                file.write(content)
            
            # Remove the old file
            os.remove(old_file_path)


def replace_schema_or_table_name(sql: str, new_schema: str = None, new_table_name: str = None, drop=False):
    create_table_pattern = r'CREATE\s+table\s+(.+\S)\s*\('
    pattern = re.compile(create_table_pattern, re.IGNORECASE + re.MULTILINE)
    match = pattern.search(sql)   
    if match:
        # Extract the table name from the first capturing group
        table_name = match.group(1)
        st = table_name.split('.')
        if len(st) == 1:
            schema, table_name = 'dbo', st[0].strip('[]')
        else:
            schema, table_name = st[-2].strip('[]'), st[-1].strip('[]')  
    else:
        raise ValueError("No table name found in the SQL statement")
 
    new_table_name = new_table_name or table_name
    new_schema = new_schema or schema
    new_table_name_full = f' {new_schema}.{new_table_name}'

    tn_pattern = fr'\s(\[?{schema}\]?\.)?\[?{table_name}\]?'
    replaced = re.sub(tn_pattern, new_table_name_full, sql)
    if drop:
        replaced = f'\nDROP TABLE IF EXISTS {new_table_name_full}; \nGO\n' + replaced
    return replaced


def clone_table_from_file(input_folder: str, entity_name: str, output_folder: str = r'.\output'):
    table_name = nc.dst_table_name(entity_name)
    table_name = table_name.split('.')[-1]  # to eliminate schema name
    table_name2 = nc.dst_table_name(nc.default_rename(entity_name)).split('.')[-1]
    file_path = find_file(root_folder=input_folder, filename=f'{table_name}.sql')
    print(file_path)
    with open(file_path, 'r', encoding='utf-8-sig') as f:  # without encoding byt order mark ï»¿ might happen
        table_def = f.read()

    stms = ''
    for new_sch, tn in [('stg', table_name), (None, table_name2)]:
        new_table_def = replace_schema_or_table_name(table_def, new_sch, tn)
        stms += new_table_def +'\n GO '
        new_file_name = os.path.join(output_folder, new_sch or 'dbo', 'Tables', f'{tn}.sql')
        print(f'writing to {new_file_name}')
        with open(new_file_name, 'w') as wf:
            wf.write(new_table_def)
    return stms


"""For batch creation"""


def clone_tables_from_file(input_folder: str, entity_names: List[str], output_folder: str = r'.\output'):
    sss = ''
    for ent in entity_names:
        ss = clone_table_from_file(input_folder, ent, output_folder)
        sss += ss + '\n'
    return sss
