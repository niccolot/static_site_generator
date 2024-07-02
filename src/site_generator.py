import re
import os
import shutil

from textnode_utils import *
from htmlnode_utils import *


def extract_single_header(markdown : str) -> str:
    
    markdown_blocks = markdown_to_blocks(markdown)

    # regex to match a single # header
    header_pattern = re.compile(r'^# (.*)$')

    headers = [header_pattern.match(block).group(1) for block in markdown_blocks if header_pattern.match(block)]

    if len(headers) != 1:
        raise Exception("There must be exactly one single # header")

    return headers[0]


def generate_page(from_path : str, template_path : str, dest_path : str) -> None:

    if not os.path.exists(from_path):
        raise Exception("markdown file not found")
    
    if not os.path.exists(template_path):
        raise Exception("html template file not found")
    
    # Get the current size of the terminal window
    columns, _ = shutil.get_terminal_size(fallback=(80, 20))
    # Print a line of '#' characters with the width of the terminal
    print('#' * columns)
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as md_file:
        markdown = md_file.read()

    with open(template_path) as template_file:
        template = template_file.read()

    html_node = markdown_to_html_node(markdown)
    contents = html_node.to_html()
    page_title = extract_single_header(markdown)

    template = template.replace("{{ Content }}", contents)
    template = template.replace("{{ Title }}", page_title)

    with open(dest_path, "w") as file:
        file.write(template)



