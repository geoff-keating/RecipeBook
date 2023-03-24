"""Formats a recipe and displays it in a markdown document"""
from enum import Enum
from pathlib import Path
from typing import Dict, Union

from jinja2 import Environment, FileSystemLoader

LOADER = FileSystemLoader(Path(__file__).parent.joinpath("templates"))

JINJA_ENV = Environment(loader=LOADER, trim_blocks=True, lstrip_blocks=True)

OUTPUT_DIR = Path(__file__).parent.joinpath("renders")


class TemplateType(Enum):
    MARKDOWN = ".md"
    HTML = '.html'


def format_recipe(
    recipe_dict: Dict, *, template_type: TemplateType = TemplateType.HTML
) -> str:
    """Format a recipe into Markdown for display"""
    template = JINJA_ENV.get_template(f"recipe_base{template_type.value}")
    render = template.render(**recipe_dict)
    file_path = OUTPUT_DIR.joinpath(
        f'{recipe_dict["recipe_name"]}{template_type.value}'
    )
    with open(file_path, "w") as fh:
        fh.write(render)
    fh.close()
    return file_path


def scale_by_factor(recipe: Dict, factor: Union[int, float]) -> Dict:
    """Scale a recipe by a certain multiple"""
    recipe["yields"]["servings"] *= factor
    for ingredient in recipe["ingredients"]:
        scaled = round(recipe["ingredients"][ingredient]["amounts"]["amount"] * factor, 1)
        recipe["ingredients"][ingredient]["amounts"]["amount"] = scaled
    return recipe


def scale_by_servings(recipe: Dict, servings: int) -> Dict:
    """Scale a recipe to make a certain number of portions"""
    factor = servings / recipe["yields"]["servings"]
    return scale_by_factor(recipe, factor)
