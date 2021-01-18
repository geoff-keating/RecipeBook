from setuptools import setup, find_packages

setup(
    name="recipe_formatter",
    author='Geoffrey Keating',
    description='package for displaying and scaling yaml formatted recipes to readable products',
    version='0.1',
    packages=['recipe_formatter'],
    entry_points={
        "console_scripts": [
            "open_recipe = recipe_formatter.open_recipe:open_recipe",
        ],
    },
    include_package_data=True
)
