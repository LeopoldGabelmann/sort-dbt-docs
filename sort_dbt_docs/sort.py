"""Sorting script for the docs markdowns.

We sort our markdown docs alphabetically. When adding or deleting docs blocks it can easily happen
that the alphabetical order is messed up. Running this script is sorting the docs alphabetically
into a new markdown file and replacing the original file with the sorted one.

In order for the script to return the desired outcome it is crucial that the format for each doc is
as follows, including the line breaks:

{% docs name_of_column %}

Description of column.

{% enddocs %}

"""
import argparse
import logging
import re


logger = logging.getLogger(__name__)


def _parse_arguments() -> argparse.Namespace:
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


def _sort_markdown(markdown_text: str) -> str:
    """Sort dbt docs macro blocs alphabetically.

    :param filename: The path to the filename that is being sorted.
    :param markdown_text: The markdown text containing the dbt macro doc blocs that need to be
        sorted.
    :return: Sorted markdown file with sorted dbt macro blocs.
    """
    pattern = r"{% docs (.+?) %}(.*?){% enddocs %}"
    docs_blocks = re.findall(pattern, markdown_text, flags=re.DOTALL)
    sorted_docs_blocks = sorted(docs_blocks, key=lambda x: x[0])

    # Add the sorted docs to a new string so that this can be written back to the file.
    sorted_markdown = ""
    for block in sorted_docs_blocks:
        sorted_markdown += (
            f"{{% docs {block[0]} %}}\n{block[1].strip()}\n{{% enddocs %}}\n\n"
        )

    # Correct the last double empty lines to only one empty line.
    sorted_markdown = sorted_markdown[:-1]
    return sorted_markdown


def sort(parser_args: argparse.Namespace) -> None:
    """Sort the docs of a dbt yml file.

    Read in the md files containing the dbt cml docs, sort the doc blocks alphabetically and
    overwrite the original file with the new content.
    """
    for filename in parser_args.filenames:
        logger.debug(f"Sorting docs within the file <{filename}>.")

        with open(file=filename, mode="r", encoding="utf-8") as f:
            markdown_text = f.read()

        sorted_markdown = _sort_markdown(markdown_text)

        # Control, whether the file has changed. If not, jump out of the function:
        if markdown_text != sorted_markdown:
            with open(file=filename, mode="w", encoding="utf-8") as f:
                f.write(sorted_markdown)
                logger.debug(f"Wrote file <{filename}>.")

            # Print to the console that there has been a resort in the files.
            print(f"The docs within <{filename}> have been sorted.")


def main():
    """Entry point for the executable."""
    args = _parse_arguments()
    raise SystemExit(sort(args))


if __name__ == "__main__":  # pragma: no cover
    args = _parse_arguments()
    raise SystemExit(sort(args))
