from typing import List, Optional
import yaml
from pydantic import BaseModel, Field


class ReplacementPattern(BaseModel):
    re_replace_this: str = Field(description="regular exrpesssion - target for search in replacement")
    replace_to: str = Field(description="string that should be used instead value that fits re_replace_this RE")


class LaunchConfig(BaseModel):
    use_source_view_clone: Optional[bool] = Field(True, description="should we use the clone of source view")
    fail_on_exception: bool = Field(True, description="if no - we are go on with batch exectuion when face some exception of one entity")
    input_folder: str = Field(None, description="path to folder with SQL files with metadata")
    output_folder: str = Field(None, description="output folder for newly created scripts")
    entities: List[str] = Field(None, description="list of entitites to process with pipeline")
    src_views_ents: Optional[List[str]] = Field(None, description="list of entitites for views to process with pipeline")
    stages: List[str] = Field(None, description="steps of execution")
    code_replacements: List[ReplacementPattern] = Field(None)
    create_view_pattern: Optional[str] = Field(description='pattern fro view creation')


def load_launch_config(file_path: str) -> LaunchConfig:
    with open(file_path, 'r') as file:
        yaml_content = yaml.safe_load(file)
    return LaunchConfig(**yaml_content)
