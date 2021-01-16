from recipe_tools.validate import validate_recipe
import yaml
import logging

logging.basicConfig(level=logging.DEBUG)

def test_correct_simple_recipe():
    recipe_path = (
        "/Users/Geoffrey/recipes/recipe_tools/testing/test_data/basic_fruit_salad.yaml"
    )
    # Load recipe
    with open(
            recipe_path,
            "r",
    ) as recipe_file:
        recipe = yaml.load(recipe_file, Loader=yaml.FullLoader)
    recipe_file.close()

    assert validate_recipe(recipe)


