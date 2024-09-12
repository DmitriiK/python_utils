from typing import List
import yaml
from pydantic import BaseModel, Field


class LaunchConfig(BaseModel):
    input_folder: str = Field(None, description="path to folder with SQL files with metadata")
    output_folder: str = Field(None, description="output folder for newly created scripts")
    entities: List[str] = Field(None, description="list of entitites to process with pipeline")
    src_views_ents: List[str] = Field(None, description="list of entitites for views to process with pipeline")


def load_launch_config(file_path: str) -> LaunchConfig:
    with open(file_path, 'r') as file:
        yaml_content = yaml.safe_load(file)
    return LaunchConfig(**yaml_content)
