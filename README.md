### Python scripts to facilitate work with SQL objects, - cloning of the tables, creation of SPs using some patterns
#### Initial  prerequesites:
For given name of entity (in terms of S&P packages it has 1 to 1 relation to "file name"), we have  some table (refered as target table) and source view.
Source view and target table usually have same chema, and 
usually their names dereives from  entity name using simple naming convention, like 
for entity "GICS_GICS" we have GICS_GICS_tbl and "GICS_GICS_Source_vw" view.
In some cases this naming conventions looks slightly different, like for "Symbol_DandBSymbol" we have Symbol_DandBSymbol_tbl but Symbol_DandB_Sourc_vw view.

#### Fuctionality
Given some set of names of the entities and for cases with no-standart naming conventions, - similar names for views we should be able
- Create clone of this table in the same schema, using differnt name, and create clone of this table in "stg" schema.
- Create clone of sourse view, and apply to SQL code of that view some tranformations, like replacements of some tables, or DB-s or whatever
- Create SP from "PULL.." category, - it pulls data from source view and inserts to newly created table in "stg" schema
- Create SP from "MERGE.." category, it pulls data from staging table and do merge to the clone of target table"
- Check the execution of the whole chaint: SourceView ->PULL_SP->StagingTable->MERGE_SP->SourceTable.


In terms of delivery it should:
- for each created or modified SQL object create DDL script and put it to git repository folder
- accumulate all this defintions in the common script(new file or clipboard), so that developer could apply it later on dev

#### Data sources.
 - Metadata related to tables schema from database
 - Defintions of tables and views from SQL scripts from Visual Studio Database projects

#### Configuration
Parameters, that supposed to be changed each launch, are configured in [yaml file] (configs\launch_configs\launch_config.yml).
Example of such file:
```yml

input_folder: 'C:\Users\dmitrii_kalmanovich\source\repos\DataFeedEngine\DataFeedEngineMI2\dbo' # folder inside Visual Studio database projects
output_folder: 'D:\Code\DatabaseBuild\Instances\DATAFEEDENGINE\Databases\DataFeedEngineMI' # folder to save resulting script, that supposed to be commited to git repo later and be a part of implementation plan

entities:
  - GICS_GICS
  - FutureEventMkt_FutureEventMktToObjectToEventType  


src_views_ents:  # for views have to create another set of names due to naming inconsistencies
  - GICS_GICS 
  - KeyDev_FutureEventMktToObjectToEventType

stages: # names of stages we are going to launch
  - CLONE_TABLE
  - CLONE_VIEW
  - CREATE_MERGE_SP
  - CREATE_PULL_SP

code_replacements: # regex parterns we are going to apply when do cloining of the vies
- re_replace_this: \[?(DatafeedEngine\]?|DatafeedEngineCache)\.\[?dbo\]?\.\[?Universe_DailyCompany_tbl\]?
  replace_to: dbo.Universe_Company2_tbl
- re_replace_this: \bCIQDataSnapshot\.
  replace_to: CIQData.
- re_replace_this: \bCREATE\s+VIEW\s+
  replace_to: "CREATE or ALTER VIEW "
```
Naming conventions, as they do not change frequqently, are hardcoded [inside python moudule] (sql\naming_convention.py)
Also need to write the proper SQL connection string here [config file] (sql/config.py)

### Launching
Main enty point is [main.py} (main.py) module. It can either take parameters from yaml config, or from command line arguments.
For dev tesing we can use set of test inside [tests] (tests) folder.
For performance tests we can use [test_flow.ipynb] (test_flow.ipynb) notebook.



