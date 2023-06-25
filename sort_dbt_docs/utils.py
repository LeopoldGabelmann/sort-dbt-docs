"""Reusable util functions for all pre-commit hooks."""
import argparse
import logging


logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse cmd arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        action="store",
        type=str,
        nargs=argparse.REMAINDER,
        help="Filename(s) in which the dbt doc blocks will be sorted alphabetically.",
    )
    parser_args = parser.parse_args()
    return parser_args
