import logging
from typing import Dict

import yaml
from cerberus import Validator

LOG = logging.getLogger(__name__)

_PLURAL_MEASURES = ["cup", "gallon", "liter", "gram"]

MEASURES = (
        ["g", "oz", "item", "each", "tsp", "tbsp"] + _PLURAL_MEASURES + [x + "s" for x in _PLURAL_MEASURES]
)

YIELD_SCHEMA = {
    "servings": {"type": "integer"},
}

INGREDIENT_SCHEMA = {
    "amounts": {
        "type": "dict",
        "schema": {
            "amount": {"type": ["integer", "float"]},
            "unit": {"type": "string", "allowed": MEASURES},
        },
    },
    "notes": {"type": "list", "schema": {"type": "string"}},
}

STEP_SCHEMA = {"steps": {"type": "list", "schema": {"type": "string"}}}


def load_recipe(recipe_path: str) -> Dict:
    """Load a recipe from a yaml file"""
    # Load recipe
    with open(
            recipe_path,
            "r",
    ) as recipe_file:
        recipe = yaml.load(recipe_file, Loader=yaml.FullLoader)
    recipe_file.close()
    return recipe


def _validate_section(section, schema):
    """Helper function for validating parts of a recipe

    Since recipes use different ingredients, the keys cannot be validated in place

    Instead, each unknown key is validated separately, hence the several schemas"""
    validator = Validator()
    if not validator.validate(section, schema):
        LOG.error(validator.errors)
        return False
    return True


def validate_recipe(recipe: Dict) -> bool:
    """Check that a recipe dictionary is valid -- see schema and cerberus docs above"""
    valid_recipe = True

    # Validate yields
    valid_recipe &= _validate_section(recipe["yields"], YIELD_SCHEMA)

    # Validate all ingredients
    for ingredient, spec in recipe["ingredients"].items():
        valid_recipe &= _validate_section(spec, INGREDIENT_SCHEMA)

    # Validate all steps
    valid_recipe &= _validate_section({"steps": recipe["steps"]}, STEP_SCHEMA)

    return valid_recipe
