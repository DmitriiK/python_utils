

import re

def extract_transaction_blocks(sql_script):
    # Split the script into blocks using comment markers
    blocks = re.split(r'(--.*?)(?=\n+--)', sql_script, flags=re.DOTALL)
    
    result = ""
    for i in range(1, len(blocks), 2):
        comment = blocks[i].strip()
        block = blocks[i+1].strip()
        
        # Check if comment starts with 'Transaction'
        if comment.startswith('--Transaction'):
            result += f"{comment}\n{block}\n\n"
    
    return result.strip()


def extract_insert_tables(sql_script):
    # Define the regex pattern for matching the INSERT INTO statements
    insert_pattern = re.compile(r"insert\s+into\s+([a-zA-Z0-9_\.]+)\s+", re.IGNORECASE)
    
    # Find all matches in the sql_script
    matches = insert_pattern.findall(sql_script)
    
    # Remove duplicates by converting to a set
    unique_tables = set(matches)
    
    # Convert back to a list if needed
    return list(unique_tables)

file_path = r'C:\Users\dmitrii_kalmanovich\source\repos\DataFeedEngine\DataFeeEngineMI\dbo\Stored Procedures\TransactionMA_ApplyChanges_prc.sql'
with open(file_path, 'r') as r:
    content=r.read()
    tb = extract_transaction_blocks(content)
    # print(tb)
lt = extract_insert_tables(tb)
output_file = r'output\globaltables.sql'
with open(output_file, 'w') as w:
    w.write('\n'.join(lt))