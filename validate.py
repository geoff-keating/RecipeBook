from cerberus import Validator
import yaml
import logging

LOG = logging.getLogger(__name__)

_PLURAL_MEASURES = ["cup", "gallon", "liter"]

MEASURES = ["g", "oz", "item", "each"] + _PLURAL_MEASURES + [x + "s" for x in _PLURAL_MEASURES]

YIELD_SCHEMA = {
    "servings": {"type": "integer"},
}

INGREDIENT_SCHEMA = {
    "amounts": {"type": "dict",
                "schema": {
                    "amount": {"type": ["integer", "float"]},
                    "unit": {"type": "string", "allowed": MEASURES}
                }
                },
    "notes": {"type": "list",
              "schema": {"type": "string"}
              }
}

STEP_SCHEMA = {
    "type": "list",
    "schema": {"type": "string"}
}


def _validate_section(section, schema):
    validator = Validator()
    if not validator.validate(section, schema):
        LOG.error(validator.errors)
        return False
    return True


def validate_recipe(recipe):
    valid_recipe = True

    # Validate yields
    valid_recipe &= _validate_section(recipe['yields'], YIELD_SCHEMA)

    # Validate all ingredients
    for ingredient in recipe['ingredients']:
        # Grab the dictionary that corresponds to the ingredient...sketchy
        specs = ingredient[list(ingredient.keys())[0]]
        valid_recipe &= _validate_section(specs, INGREDIENT_SCHEMA)

    # Validate all steps

    return valid_recipe
