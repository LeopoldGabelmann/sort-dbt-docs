"""Unit test the file sort_dbt_docs/sort_dbt_docfiles.py."""
import argparse
import os
from pathlib import Path
from unittest import mock

import pytest

from sort_dbt_docs.sort_dbt_docfiles import _sort_markdown
from sort_dbt_docs.sort_dbt_docfiles import sort

# Define constants.
TEST_DATA = Path(os.path.abspath(os.curdir)) / "tests/testdata"


@pytest.fixture
def set_argparse_namespace():
    """Fixture that sets a argparse namespace with one file name as input."""
    parser = argparse.Namespace(filenames=["file_one"])
    return parser


@pytest.fixture
def get_input_docs():
    """Fixture that returns a path to a test doc markdown file."""

    def _method(scenario: str) -> str:
        if scenario == "happy":
            filename = "happy_docs.md"
        elif scenario == "double":
            filename = "double_docs.md"
        elif scenario == "double_no_sort":
            filename = "double_no_sort_docs.md"
        elif scenario == "to_sort":
            filename = "to_sort_docs.md"
        elif scenario == "special_signs":
            filename = "special_signs_docs.md"
        elif scenario == "no_empty_lines":
            filename = "no_empty_lines_docs.md"
        elif scenario == "cap_low":
            filename = "cap_low_docs.md"
        else:
            raise ValueError("Senario is not defined.")

        file_path = TEST_DATA / filename
        with open(file=file_path, encoding="utf-8") as f:
            markdown_text = f.read()
        return markdown_text

    return _method


@pytest.fixture
def get_expected_docs():
    """Fixture that outputs the expected format of the docs after the sorting."""

    def _method(scenario: str) -> str:
        if scenario == "double":
            filename = "expected_double_docs.md"
        elif scenario == "double_no_sort":
            filename = "expected_double_no_sort_docs.md"
        elif scenario == "to_sort":
            filename = "happy_docs.md"
        elif scenario == "special_signs":
            filename = "expected_special_signs_docs.md"
        elif scenario == "no_empty_lines":
            filename = "expected_no_empty_lines_docs.md"
        elif scenario == "cap_low":
            filename = "expected_cap_low_docs.md"
        elif scenario == "happy":
            filename = "happy_docs.md"
        else:
            raise ValueError("Scenario is not defined.")

        file_path = TEST_DATA / filename
        with open(file=file_path, encoding="utf-8") as f:
            markdown_text = f.read()
        return markdown_text

    return _method


class TestSortMarkdown:
    """Unit tests for the function _sort_markdown()."""

    @pytest.mark.parametrize(
        "scenario",
        ["happy", "to_sort", "double", "special_signs", "no_empty_lines", "cap_low"],
    )
    def test_sort_docs(self, scenario, get_input_docs, get_expected_docs):
        """Test that the docs are sorted as expected."""
        docs, expected = get_input_docs(scenario), get_expected_docs(scenario)

        result = _sort_markdown(markdown_text=docs)
        assert result == expected


class TestSort:
    """All unit test for the sort() function."""

    def test_main_no_write(self, get_input_docs, set_argparse_namespace):
        """Test that if the docs are not sorted, main() does not write anything."""
        with mock.patch(
            "builtins.open", mock.mock_open(read_data=get_input_docs("happy"))
        ) as mock_open_file:
            sort(set_argparse_namespace)

        mock_open_file.assert_called_once_with(
            file="file_one", mode="r", encoding="utf-8"
        )
        mock_open_file.return_value.__enter__().write.assert_not_called()

    def test_main_write(
        self, get_input_docs, get_expected_docs, set_argparse_namespace
    ):
        """Test that main() writes the expected sorted docs."""
        scenario = "double"
        expected = get_expected_docs(scenario)

        with mock.patch(
            "builtins.open", mock.mock_open(read_data=get_input_docs(scenario))
        ) as mock_open_file:
            sort(set_argparse_namespace)

        mock_open_file.return_value.__enter__().write.assert_called_with(expected)

    def test_main_multiple_calls(self, get_input_docs):
        """Test that main() iterates over multiple files, if given multiple parser arguments."""
        parser = argparse.Namespace(filenames=["file_one", "file_two"])

        with mock.patch(
            "builtins.open", mock.mock_open(read_data=get_input_docs("to_sort"))
        ) as mock_open_file:
            sort(parser)

        assert mock_open_file.call_count == 4
        assert mock_open_file.call_args_list[0].kwargs["file"] == "file_one"
        assert mock_open_file.call_args_list[0].kwargs["mode"] == "r"
        assert mock_open_file.call_args_list[1].kwargs["file"] == "file_one"
        assert mock_open_file.call_args_list[1].kwargs["mode"] == "w"
        assert mock_open_file.call_args_list[2].kwargs["file"] == "file_two"
        assert mock_open_file.call_args_list[2].kwargs["mode"] == "r"
        assert mock_open_file.call_args_list[3].kwargs["file"] == "file_two"
        assert mock_open_file.call_args_list[3].kwargs["mode"] == "w"

    def test_two_calls_only_one_write(self, get_input_docs):
        """
        Test if only one file is written if the first call is for a file that is already sorted.
        """

        def mapped_mock_open(mapping_dict):
            def _side_effect(file, *args, **kwargs):
                return mock_files[file]

            mock_files = {}
            for key, value in mapping_dict.items():
                mock_files[key] = mock.mock_open(read_data=value).return_value

            mock_opener = mock.Mock()
            mock_opener.side_effect = _side_effect
            return mock_opener

        parser = argparse.Namespace(filenames=["file_one", "file_two"])
        mapping_dict = {
            "file_one": get_input_docs("happy"),
            "file_two": get_input_docs("to_sort"),
        }

        with mock.patch(
            "builtins.open", mapped_mock_open(mapping_dict)
        ) as mock_open_file:
            sort(parser)

        assert mock_open_file.call_count == 3
        assert mock_open_file.call_args_list[0].kwargs["mode"] == "r"
        assert mock_open_file.call_args_list[1].kwargs["mode"] == "r"
        assert mock_open_file.call_args_list[2].kwargs["mode"] == "w"
