"""Sorting script for all dbt yaml files for the model setup and documentation.

A dbt yml file for dbt models usually consists out of a config block, sources and models. This hook
sorts it into this structure

config block
sources
models.
"""
import argparse
import logging
from operator import itemgetter

import yaml

from sort_dbt_docs.utils import parse_arguments

logger = logging.getLogger(__name__)


def _sort_yaml(yaml_dict: dict) -> dict:
    """Sort dbt model yaml files alphabetically.

    :param yaml_dict: The content of the yaml file to sort as a string.
    :return: The sorted content of the yaml file as a string.
    """
    dict_keys = yaml_dict.keys()

    # sort all non sources and models keys to the top in alphabetical order.
    main_keys = ["sources", "models"]
    config_keys = sorted([key for key in dict_keys if key not in main_keys])

    sorted_dict = {}
    for key in config_keys:
        sorted_dict[key] = yaml_dict[key]

    non_config_keys = [key for key in dict_keys if key in main_keys]
    if "sources" in non_config_keys:
        sorted_sources = []
        for source in sorted(yaml_dict["sources"], key=itemgetter("name")):
            tables = source.pop("tables")
            sorted_tables = sorted(tables, key=itemgetter("name"))
            source["tables"] = sorted_tables
            sorted_sources.append(source)
        sorted_dict["sources"] = sorted_sources
    if "models" in non_config_keys:
        sorted_models = sorted(yaml_dict["models"], key=itemgetter("name"))
        sorted_dict["models"] = sorted_models

    return sorted_dict


def sort(parser_args: argparse.Namespace) -> None:
    """Sort a dbt yaml file.

    Read in the original yaml file and change the order of the blocks to config, sources, models
    and within those blocks to an alphabetical order.
    """
    for filename in parser_args.filenames:
        logger.debug(f"Sorting keys and values from the yaml in file <{filename}>.")
        yml_text = yaml.safe_load(filename)
        sorted_yml = _sort_yaml(yml_text)

        # Control, whether the file has changed. If not, do nothing.
        if str(yml_text) != str(sorted_yml):
            with open(file=filename, mode="w", encoding="utf-8") as f:
                yaml.dump(sorted_yml, f)
                logger.debug(f"Dumped yaml file <{filename}>.")

            # Print to console that there have been adjustments within the yaml file.
            print(f"The yaml file <{filename}> has been re-sorted.")


def main():
    """Entry point for the executable."""
    args = parse_arguments()
    raise SystemExit(sort(args))


if __name__ == "__main__":
    main()
