"""Unit test the file sort_dbt_docs/utils.py."""
from unittest import mock

from sort_dbt_docs.utils import parse_arguments


class TestParser:
    """All unit test for the parse_arguments() function."""

    @mock.patch("sys.argv", ["script.py", "file1.md", "file2.md"])
    def test_parser_nargs(self):
        """Test that the parser reads in the remainders as filenames."""
        args = parse_arguments()

        assert args.filenames == ["file1.md", "file2.md"]

    @mock.patch("sys.argv", ["script.py"])
    def test_parser_no_args(self):
        """Test that the parser is empty if no remainders are given."""
        args = parse_arguments()

        assert args.filenames == []
