"""Unit test the file sort_dbt_docs/sort.py,"""
import argparse
import os
from pathlib import Path
from unittest import mock

import pytest

from sort_dbt_docs.sort import _parse_arguments
from sort_dbt_docs.sort import _sort_markdown
from sort_dbt_docs.sort import main


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


class TestParser:
    """All unit test for the parse_arguments() function."""

    @mock.patch("sys.argv", ["script.py", "file1.md", "file2.md"])
    def test_parser_nargs(self):
        """Test that the parser reads in the remainders as filenames."""
        args = _parse_arguments()

        assert args.filenames == ["file1.md", "file2.md"]

    @mock.patch("sys.argv", ["script.py"])
    def test_parser_no_args(self):
        """Test that the parser is empty if no remainders are given."""
        args = _parse_arguments()

        assert args.filenames == []


class TestSortMarkdown:
    """Unit tests for the function sort()."""

    @pytest.mark.parametrize(
        "scenario",
        ["happy", "to_sort", "double", "special_signs", "no_empty_lines", "cap_low"],
    )
    def test_sort_double_docs(self, scenario, get_input_docs, get_expected_docs):
        """Test that the docs are sorted as expected."""
        docs, expected = get_input_docs(scenario), get_expected_docs(scenario)

        result = _sort_markdown(markdown_text=docs)
        assert result == expected


class TestMain:
    """All unit test for the main() function."""

    def test_main_no_write(self, get_input_docs, set_argparse_namespace):
        """Test that if the docs are not sorted, main() does not write anything."""
        with mock.patch(
            "builtins.open", mock.mock_open(read_data=get_input_docs("happy"))
        ) as mock_open_file:
            main(set_argparse_namespace)

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
            main(set_argparse_namespace)

        mock_open_file.return_value.__enter__().write.assert_called_with(expected)

    def test_main_multiple_calls(self, get_input_docs):
        """Test that main() iterates over multiple files, if given multiple parser arguments."""
        parser = argparse.Namespace(filenames=["file_one", "file_two"])

        with mock.patch(
            "builtins.open", mock.mock_open(read_data=get_input_docs("to_sort"))
        ) as mock_open_file:
            main(parser)

        assert mock_open_file.call_count == 4
        assert mock_open_file.call_args_list[0].kwargs["file"] == "file_one"
        assert mock_open_file.call_args_list[0].kwargs["mode"] == "r"
        assert mock_open_file.call_args_list[1].kwargs["file"] == "file_one"
        assert mock_open_file.call_args_list[1].kwargs["mode"] == "w"
        assert mock_open_file.call_args_list[2].kwargs["file"] == "file_two"
        assert mock_open_file.call_args_list[2].kwargs["mode"] == "r"
        assert mock_open_file.call_args_list[3].kwargs["file"] == "file_two"
        assert mock_open_file.call_args_list[3].kwargs["mode"] == "w"
