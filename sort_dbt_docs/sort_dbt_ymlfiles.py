"""Sorting script for all dbt yaml files for the model setup and documentation.

A dbt yml file for dbt models usually consists out of a config block, sources and models. This hook
sorts this structure

config block
sources
models.
"""
import logging

from sort_dbt_docs.utils import parse_arguments


logger = logging.getLogger(__name__)


def _sort_yaml(yaml_text: str) -> str:
    """Sort dbt model yaml files alphabetically.

    :param yaml_text: The content of the yaml file to sort as a string.
    :return: The sorted content of the yaml file as a string.
    """
    return yaml_text
