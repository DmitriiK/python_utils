
import pyperclip
import os

from sql.utils import get_table_schema_db


def output_to_file(output_folder: str, object_type: str, object_name: str, object_def: str):
    on, sn, _ = get_table_schema_db(object_name)
    directory_path = os.path.join(output_folder, sn, object_type)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_path = os.path.join(directory_path, f'{on}.sql')
    print('writing to ', file_path)
    with open(file_path, 'w') as f:
        f.write(object_def)


def output_to_clipboard(object_def: str):
    pyperclip.copy(object_def)
    print(f'string like "{object_def[0:50]}... " with len {len(object_def)} has been copied to clipboard')

