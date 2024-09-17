import os
import re


def split_sql_file(input_file, output_folder):
    with open(input_file, 'r') as file:
        content = file.read()
    
    # Split the content by "GO "
    sql_statements = re.split(r'\bGO\b', content, flags=re.IGNORECASE)
    
    for statement in sql_statements:
        statement = statement.strip()
        if not statement:
            continue
        
        # Check for CREATE TABLE or CREATE OR ALTER statements
        match = re.search(r'CREATE\s+(TABLE|OR\s+ALTER\s+(VIEW|PROCEDURE))\s+(\[?(\w+)\]?\.\[?(\w+)\]?)', statement, re.IGNORECASE)
        if match:
            schema_name = match.group(4)
            object_name = match.group(5)
            
            # Create schema directory if it doesn't exist
            schema_dir = os.path.join(output_folder, schema_name)
            os.makedirs(schema_dir, exist_ok=True)
            
            # Write the statement to a new file
            file_path = os.path.join(schema_dir, f"{object_name}.sql")
            with open(file_path, 'w') as out_file:
                out_file.write(statement)


def test_spit():
    file_name = r'C:\Users\dmitrii_kalmanovich\Documents\SQL Server Management Studio\transactions_stuff.sql'
    output_folder = r'output\split_output'
    split_sql_file(file_name, output_folder)
