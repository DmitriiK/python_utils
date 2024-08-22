import os
import re

def merge_sql_files(input_folder, output_file):
        # Define the regex pattern
    pattern = re.compile(r'^russel.*_stg_.*\.sql$', re.IGNORECASE)
    
    # Get all files in the input folder
    all_files = os.listdir(input_folder)

    # Filter files based on regex pattern
    sql_files = [f for f in all_files if pattern.match(f)] 
    xx =''
    for sql_file in sql_files:
        with open(os.path.join(input_folder, sql_file), 'r', encoding='utf-8-sig') as infile:
            x = infile.read()
            xx += x + '\nGO\n'
            
    with open(output_file, 'w',  encoding='UTF-8') as outfile:
        outfile.write(xx)

if __name__ == "__main__":
    input_folder = r'C:\Users\dmitrii_kalmanovich\source\repos\DataFeedEngine\DataFeedEngineIndex-Backup-20220722\dbo\Tables'  # Update this with your folder path
    output_file = r'merge_output.sql'  # Update this with your output file path
    
    merge_sql_files(input_folder, output_file)