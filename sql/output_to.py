
import pyperclip


def output_to_file(file_path: str, object_def: str):
    print('writing to ', file_path) 
    with open(file_path, 'w') as f:
        f.write(object_def)


def output_to_clipboard(object_def: str):
    pyperclip.copy(object_def)

def output_to_sql(object_def: str):
    pyperclip.copy(object_def)