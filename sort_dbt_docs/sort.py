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


def main():
    """Sort the docs of a dbt yml file.

    Read in the yml containing the dbt cml docs, sort the doc blocks alphabetically and overwrite
    the original file with the new content.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        action="store",
        type=str,
        nargs=argparse.REMAINDER,
        help="Filename in which the dbt doc blocks will be sorted alphabetically.",
    )
    args = parser.parse_args()

    for filename in args.filenames:
        logger.debug(f"Sorting docs within the file <{filename}>.")

        with open(filename) as f:
            markdown_text = f.read()

        pattern = r"{% docs (.+?) %}\n(.*?)\n{% enddocs %}"
        docs_blocks = re.findall(pattern, markdown_text, flags=re.DOTALL)
        sorted_docs_blocks = sorted(docs_blocks, key=lambda x: x[0].lower())

        # Add the sorted docs to a new string so that this can be written back to the file.
        sorted_markdown = ""
        for block in sorted_docs_blocks:
            sorted_markdown += (
                f"{{% docs {block[0]} %}}\n{block[1]}\n{{% enddocs %}}\n\n\n"
            )

        # Correct the last three empty lines to only one empty line.
        sorted_markdown = sorted_markdown[:-2]
        logger.debug(f"Deleted the last two line breaks of the file <{filename}>.")

        # Control, whether the file has changed. If not, jump out of the function:
        if markdown_text != sorted_markdown:
            with open(filename, "w") as f:
                f.write(sorted_markdown)
                logger.debug(f"Wrote file <{filename}>.")

            # Print to the console that there has been a resort in the files.
            print(f"The docs within <{filename}> have been sorted.")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
