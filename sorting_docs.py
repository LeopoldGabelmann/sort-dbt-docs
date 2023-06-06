''' Sorting script for the docs markdowns.

We sort our markdown docs alphabetically. When adding or deleting docs blocks it can easily happen
that the alphabetical order is messed up. Running this script is sorting the docs alphabetically 
into a new markdown file and replacing the original file with the sorted one.

In order for the script to return the desired outcome it is crucial that the format for each doc is
as follows, including the line breaks: 

{% docs name_of_column %}

Description of column.

{% enddocs %}

'''

import os
import re
import shutil

# Get the list of markdown files in the folder
folder_path = 'macros\docs'  # Set the folder path where the markdown files are located
markdown_files = [file for file in os.listdir(folder_path) if file.startswith('doc_') and file.endswith('.md')]

# Sort and replace each markdown file
for file_name in markdown_files:
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, 'r') as f:
        markdown_text = f.read()

    pattern = r'{% docs (.+?) %}\n(.*?)\n{% enddocs %}'
    docs_blocks = re.findall(pattern, markdown_text, flags=re.DOTALL)

    sorted_docs_blocks = sorted(docs_blocks, key=lambda x: x[0].lower())

    sorted_markdown = ''
    for block in sorted_docs_blocks:
        sorted_markdown += f'{{% docs {block[0]} %}}\n{block[1]}\n{{% enddocs %}}\n\n\n'

    # Create a temporary file path for the sorted markdown
    temp_file_path = file_path + '.temp'

    with open(temp_file_path, 'w') as f:
        f.write(sorted_markdown)

    # Replace the original file with the sorted file
    shutil.move(temp_file_path, file_path)
