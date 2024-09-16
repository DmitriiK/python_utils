from typing import List
import yaml
from pydantic import BaseModel, Field


class ReplacementPattern(BaseModel):
    re_replace_this: str = Field(None, description="regular exrpesssion - target for search in replacement")
    replace_to: str = Field(None, description="string that should be used instead value that fits re_replace_this RE")


class LaunchConfig(BaseModel):
    input_folder: str = Field(None, description="path to folder with SQL files with metadata")
    output_folder: str = Field(None, description="output folder for newly created scripts")
    entities: List[str] = Field(None, description="list of entitites to process with pipeline")
    src_views_ents: List[str] = Field(None, description="list of entitites for views to process with pipeline")
    stages: List[str] = Field(None, description="steps of execution")
    code_replacements: List[ReplacementPattern] = Field(None)


def load_launch_config(file_path: str) -> LaunchConfig:
    with open(file_path, 'r') as file:
        yaml_content = yaml.safe_load(file)
    return LaunchConfig(**yaml_content)
