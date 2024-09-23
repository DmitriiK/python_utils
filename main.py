import argparse
import logging
import pyperclip

from configs.lauch_config import load_launch_config, LaunchConfig
# from file_parsing.file_utils import clone_tables_from_file
from sql.sql_requests import SQL_Communicator, SQL_OBJECT_TYPE

default_launch_config_path = r'configs\launch_configs\launch_config.yml'
# Initialize parser
parser = argparse.ArgumentParser()


def setup_args():
    parser.add_argument("-lc", "--launch_config_path", help="path to launch config file")
    parser.add_argument("-of", "--output_folder", help="output folder for newly created scripts")
    parser.add_argument("-if", "--input_folder", help="input folder with sql files for parsing")
    parser.add_argument("-ent", "--entities", help="commal delimetered list of entitiies to process")
    parser.add_argument("-sve", "--src_views_ents", help="commal delimetered list of entitiies to process for views")
    parser.add_argument("-st", "--stages", help="commal delimetered list of stages(steps) ")


def launch_stage(mdr: SQL_Communicator, stage: str, cfg: LaunchConfig):
    match stage:
        case 'CLONE_TABLE':
            tables_def = mdr.create_new_sql_object(ot=SQL_OBJECT_TYPE.TABLE, ents=cfg.entities, output_dir=cfg.output_folder)
            return tables_def
            #  nc_view_name=nc.source_view_name to do configuration
        case 'CLONE_STG_TABLE':
            tables_def = mdr.create_new_sql_object(ot=SQL_OBJECT_TYPE.STG_TABLE, ents=cfg.entities, output_dir=cfg.output_folder)
            return tables_def
        case 'CLONE_VIEW':
            view_defs = mdr.create_new_sql_object(ot=SQL_OBJECT_TYPE.VIEW, ents=cfg.entities, output_dir=cfg.output_folder,
                                                  rppts=cfg.code_replacements)
            return view_defs
            #  nc_view_name=nc.source_view_name to do configuration
        case 'CREATE_PULL_SP':
            sp_defs = mdr.create_new_sql_object(ot=SQL_OBJECT_TYPE.PULL_SP, ents=cfg.entities, src_views_ents=cfg.src_views_ents,
                                                output_dir=cfg.output_folder)
            return sp_defs
        case 'CREATE_MERGE_SP':
            sp_defs = mdr.create_new_sql_object(ot=SQL_OBJECT_TYPE.MERGE_SP, ents=cfg.entities, output_dir=cfg.output_folder)
            return sp_defs
        case _:
            logging.warning(f'stage {stage} not defined')


def main():
    setup_args()

    args = parser.parse_args()
    args_count = sum([1 for arg in vars(args).values() if arg is not None])
    if not args_count:
        cfg = load_launch_config(default_launch_config_path)
    else:
        if args.launch_config_path:
            cfg = load_launch_config(args.launch_config_path)
        else:
            cfg = LaunchConfig(input_folder=args.input_folder, output_folder=args.input_folder, entities=args.entities.split(','))
            if args.src_views_ents:
                cfg.src_views_ents = args.src_views_ents.split(',')
    logging.info(cfg)
    ss = ''  # string with sql script to copy to clipboard
    with SQL_Communicator() as mdr:
        for stage in cfg.stages:
            logging.info(f'------launching state {stage}----------')
            stage_script = launch_stage(mdr, stage, cfg)
            ss += stage_script

    pyperclip.copy(ss)


if __name__ == "__main__":
    main()
