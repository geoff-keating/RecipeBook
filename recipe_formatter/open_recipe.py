"""Entry point for loading, scaling, and displaying recipes"""
import argparse
import webbrowser

from recipe_formatter.format_recipe import (
    scale_by_factor,
    scale_by_servings,
    format_recipe,
    TemplateType,
)
from recipe_formatter.validate import load_recipe, validate_recipe


def open_recipe():
    """Open a recipe file in a web browser"""
    parser = argparse.ArgumentParser()
    parser.add_argument("recipe_path", type=str, help="Path to a recipe file")
    parser.add_argument(
        "--type",
        dest='template_type',
        type=str,
        choices=[tt.name for tt in TemplateType],
        default=TemplateType.HTML,
        help="Output file type",
    )

    scalers = parser.add_mutually_exclusive_group()
    scalers.add_argument(
        "--servings",
        type=int,
        default=None,
        help="Scale the recipe to a number of servings",
    )
    scalers.add_argument(
        "--scale", type=float, default=None, help="Scale the recipe by a factor"
    )

    args = parser.parse_args()
    recipe = load_recipe(args.recipe_path)
    if not validate_recipe(recipe):
        raise ValueError('Invalid recipe')
    if args.servings:
        recipe = scale_by_servings(recipe, args.servings)
    if args.scale:
        recipe = scale_by_factor(recipe, args.scale)
    render_path = format_recipe(recipe, template_type=args.template_type)
    webbrowser.get().open(f"file:///{render_path}")
