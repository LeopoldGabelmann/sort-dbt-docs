"""Unit test the file sort_dbt_docs/sort_dbt_yamlfiles.py"""
import argparse
import os
from pathlib import Path
from unittest import mock

import pytest
import yaml

from sort_dbt_docs.sort_dbt_yamlfiles import _sort_yaml
from sort_dbt_docs.sort_dbt_yamlfiles import sort

# Define constants.
TEST_DATA = Path(os.path.abspath(os.curdir)) / "tests" / "testdata" / "yamls"


@pytest.fixture
def set_argparse_namespace():
    """Fixture that sets a argparse namespace with one file name as input."""
    parser = argparse.Namespace(filenames=["yaml_one.yaml"])
    return parser


@pytest.fixture
def get_input_yaml():
    """Fixture that returns a path to a test yaml file."""

    def _method(scenario: str) -> str:
        if scenario == "happy":
            filename = "happy_yaml.yaml"
        elif scenario == "double":
            filename = "double_yaml.yaml"
        elif scenario == "to_sort":
            filename = "to_sort_yaml.yaml"
        else:
            raise ValueError("Senario is not defined.")

        file_path = TEST_DATA / filename
        with open(file_path) as f:
            yaml_dict = yaml.safe_load(f)
        return yaml_dict

    return _method


@pytest.fixture
def get_expected_yaml():
    """Fixture that outputs the expected format of the docs after the sorting."""

    def _method(scenario: str) -> str:
        if scenario == "double":
            filename = "expected_double_yaml.yaml"
        elif scenario == "to_sort":
            filename = "expected_to_sort_yaml.yaml"
        else:
            raise ValueError("Scenario is not defined.")

        file_path = TEST_DATA / filename
        with open(file_path) as f:
            yaml_dict = yaml.safe_load(f)
        return yaml_dict

    return _method


class TestSort:
    """All unit tests for the sort() function."""

    @mock.patch("yaml.dump")
    def test_sort_no_dump(self, mock_yaml_dump, get_input_yaml, set_argparse_namespace):
        """Test that if the yaml is not sorted, sort() does not write anything."""
        input_yaml = get_input_yaml("happy")

        with mock.patch(
            "yaml.safe_load", return_value=input_yaml
        ) as mock_yaml_load, mock.patch("builtins.open"):
            sort(set_argparse_namespace)

        mock_yaml_load.assert_called_once_with("yaml_one.yaml")
        assert mock_yaml_dump.call_count == 0

    @mock.patch("yaml.dump")
    def test_sort_dump(self, mock_yaml_dump, get_input_yaml, set_argparse_namespace):
        """Test that sort() dumps a file."""
        with mock.patch(
            "yaml.safe_load", return_value=get_input_yaml("to_sort")
        ), mock.patch("builtins.open"):
            sort(parser_args=set_argparse_namespace)

        assert mock_yaml_dump.call_count == 1

    @mock.patch("yaml.dump")
    def test_sort_multiple_calls(self, mock_yaml_dump, get_input_yaml):
        """Test that sort() iterates over mutiple files, if given multiple parser arguments."""
        parser = argparse.Namespace(filenames=["yaml_one..yaml", "yaml_two.yaml"])

        with mock.patch(
            "yaml.safe_load", return_value=get_input_yaml("to_sort")
        ) as mock_yaml_load, mock.patch("builtins.open"):
            sort(parser)

        assert mock_yaml_load.call_count == 2
        assert mock_yaml_dump.call_count == 2

    @mock.patch("yaml.dump")
    def test_sort_two_calls_only_one_write(self, mock_yaml_dump, get_input_yaml):
        """Test that only one file is written back if given one sorted and one messy yaml file."""
        mock_yaml_dump.return_value = None
        to_sort_docs = get_input_yaml("to_sort")
        no_sort_docs = get_input_yaml("happy")

        def _side_effect(stream):
            if stream == "yaml_one.yaml":
                return to_sort_docs
            else:
                return no_sort_docs

        parser = argparse.Namespace(filenames=["yaml_one.yaml", "yaml_two.yaml"])

        with mock.patch("yaml.safe_load") as mock_yaml_load, mock.patch(
            "builtins.open"
        ):
            mock_yaml_load.side_effect = _side_effect
            sort(parser)

        assert mock_yaml_load.call_count == 2
        assert mock_yaml_dump.call_count == 1
