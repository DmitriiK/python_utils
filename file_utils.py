import os
import re

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

# Example usage
folder_path = r'D:\Code\DatabaseBuild\Instances\DATAFEEDENGINE\Databases\DataFeedEngineIndex\stg\Tables'
rename_and_modify_sql_files(folder_path)
