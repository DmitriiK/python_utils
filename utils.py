import os
import glob
import shutil
from typing import List
import pyperclip

root_folder = r'C:\Users\dmitrii_kalmanovich\source\repos\DataFeedEngine'
def batch_copy_files(input_folder, file_mask, output_folder = None):
    # Get a list of files matching the specified mask
    matching_files = glob.glob(os.path.join(input_folder, file_mask))

    # Iterate through each matching file
    for original_file_path in matching_files:
        # Extract the file name and extension
        file_name, file_extension = os.path.splitext(os.path.basename(original_file_path))

        # Modify the file name (prepend "RussellUS2")
        new_file_name = f'{file_name}{file_extension}'.replace("US_", "US2_")
        if not output_folder:
            output_folder = input_folder
        new_file_path = os.path.join(output_folder, new_file_name)

        # Copy the file to the new locat'zion
        shutil.copy(original_file_path, new_file_path)
        print(f"File copied: {original_file_path} -> {new_file_path}")

def clone_file_to_many(inp_folder:str, ent_s: str, name_template: str, content_template: str):
    lst = ent_s.split(',')
    for ent in lst:
        ent = ent.strip()
        new_name = name_template.format(ent)
        new_path =os.path.join(inp_folder, new_name)
        print(f'making file as as {new_path}')
        content_str = content_template.format(ent)
        with open(new_path, 'w') as f:
            f.write(content_str)



def test_batch_copy():
    input_folder = root_folder+ r"\DataFeedEngineIndex\dbo\Tables"
    output_folder = r'C:\Users\dmitrii_kalmanovich\source\tmp'
    file_mask = "RussellUS_*.*"
    batch_copy_files(input_folder, file_mask, output_folder)

def test_clone_file_to_many():
    inp_folder = r'C:\Users\dmitrii_kalmanovich\source\repos\DataFeedEngine\DataFeedEngineIndex\dbo\Stored Procedures\Procs1'
    name_template = 'MergeData_RussellUS2_{0}_prc.sql'
    ents = """
            ConstituentIdentifier,
            ConstituentLevel,
            IdentifierType,
            IndexConstituentLevel,
            IndexConstituentValue5Year,
            IndexConstituentValue,
            IndexConstituent,
            IndexCorporateAction5Year,
            IndexCorporateAction,
            IndexICAType,
            IndexLevel,
            IndexProvider,
            IndexRelLevel,
            IndexRel,
            IndexSecurityTextCurrent5year,
            IndexSecurityTextCurrent,
            IndexSecurityValue5Year,
            IndexSecurityValue,
            IndexTradingItemLevel,
            IndexTradingItem,
            IndexValue5Year,
            IndexValueLevel,
            IndexValue,
            Index
    """
    file_content_template = """-- EXEC [MergeData_RussellUS2_{0}_prc]
        CREATE   PROCEDURE [dbo].[MergeData_RussellUS2_{0}_prc]    
        AS    
        BEGIN
            MERGE [dbo].[RussellUS2_{0}_tbl] AS DST
            USING   stg.RussellUS2_{0}_tbl as SRC WITH (NOLOCK)
                ON DST.[{0}Id] = SRC.[{0}Id] 
                AND DST.[{0}ProviderID] = SRC.[{0}ProviderID] 
            WHEN MATCHED 
                AND (
                    ISNULL(DST.[{0}Name], '') <> ISNULL(SRC.[{0}Name], '') 
                ) THEN 
                UPDATE SET 
                    [{0}Name] = SRC.[{0}Name]			
            WHEN NOT MATCHED BY TARGET THEN
                INSERT ([{0}Id], [{0}ProviderID], [{0}Name])
                VALUES (SRC.[{0}Id], SRC.[{0}ProviderID], SRC.[{0}Name])
            WHEN NOT MATCHED BY SOURCE THEN
                DELETE 
            ;
        END
        """

def generate_merge_stm(tbl_srs: str, tbl_dst: str, cols: str, pk_cols_ordinal = 1):
    lst = [x.strip() for x in cols.split(',')]
    insrt = ', '.join(lst)
    insrt2 = ', '.join([f'SRC.{x}' for x in lst])

    pk_cols = lst[0:pk_cols_ordinal]
    join_cond = 'AND '.join([f'DST.{x} = SRC.{x}' for x in pk_cols])
    non_pk_cols = list(set(lst) - set(pk_cols))
    update_part= ',\n'.join([f'{x} = SRC.{x}' for x in non_pk_cols])
    update_cond = ' AND '.join([f"ISNULL(DST.{x}, '') <> ISNULL(SRC.{x}, '') " for x in non_pk_cols])

    stm = f""" MERGE {tbl_dst} AS DST
            USING   {tbl_srs} as SRC WITH (NOLOCK)
                ON {join_cond}
            WHEN MATCHED 
                AND (
                    {update_cond}
                ) THEN 
                UPDATE SET 
                   {update_part}			
            WHEN NOT MATCHED BY TARGET THEN
                INSERT ({insrt})
                VALUES ({insrt2})
            WHEN NOT MATCHED BY SOURCE THEN
                DELETE 
            ;;"""
    print(stm)
    return stm

def test_generate_merge_stm():
    src_tbl = 'stg.RussellUS2_ConstituentIdentifier_tbl '
    dst_tbl = 'dbo.RussellUS2_ConstituentIdentifier_tbl'
    cols = """
     [constituentId],
    [identifierTypeId],
    [fromDate],
    [identifierValue],
    [toDate]
    """
    pko = 3
    stm = generate_merge_stm(src_tbl, dst_tbl, cols, pko)
    pyperclip.copy(stm)


test_batch_copy()

    