import logging
from pathlib import Path

import pytest

from recipe_formatter.format_recipe import format_recipe
from recipe_formatter.validate import load_recipe, validate_recipe

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def sample_recipe():
    file_path = Path(__file__).parent.joinpath("test_data").joinpath("fruit_salad.yaml")
    return load_recipe(file_path)


@pytest.fixture
def sample_displayed():
    file_path = Path(__file__).parent.joinpath("test_data").joinpath("fruit_salad.md")
    with open(file_path, "r") as fmd:
        raw = fmd.read()
    fmd.close()
    return raw


# TODO: make exhaustive...
def test_validation(sample_recipe):
    """Test validating a sample recipe"""
    assert validate_recipe(sample_recipe)


def test_display_recipe(sample_recipe, sample_displayed):
    """Test recipe display script"""
    rendered = format_recipe(sample_recipe)
    assert rendered == sample_displayed
