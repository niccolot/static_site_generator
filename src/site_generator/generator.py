import re
import os
import shutil

from site_generator.textnode_utils import *
from site_generator.htmlnode_utils import *


def copy_static_contents(dir1 : str, dir2 : str) -> None:

    if not os.path.exists(dir1):
        raise Exception("Static contents directory not found")

    if os.path.exists(dir2):
        print(f"Erasing old contents from '{dir2}' directory")
        shutil.rmtree(dir2)

    print(f"Creating new '{dir2}' directory")
    os.mkdir(dir2)

    if os.path.exists(dir1):

        dir1_contents = os.listdir(dir1)

        for elem in dir1_contents:
            if os.path.isfile(f"{dir1}/{elem}"):
                print(f"Copying of '{dir1}/{elem}' to '{dir2}/{elem}'")
                shutil.copy(f"{dir1}/{elem}", f"{dir2}/{elem}")
            else:
                print(f"Creating directory '{dir2}/{elem}'")
                os.mkdir(f"{dir2}/{elem}")
                print(f"Transferring files from '{dir1}/{elem}' to '{dir2}/{elem}'")
                copy_static_contents(f"{dir1}/{elem}", f"{dir2}/{elem}")
    else:
        shutil.copy(f"{dir1}", f"{dir2}")



def extract_single_header(markdown : str) -> str:
    
    markdown_blocks = markdown_to_blocks(markdown)

    # regex to match a single # header
    header_pattern = re.compile(r'^# (.*)$')

    headers = [header_pattern.match(block).group(1) for block in markdown_blocks if header_pattern.match(block)]

    if len(headers) != 1:
        raise Exception("There must be exactly one single # header")

    return headers[0]


def generate_page(from_path : str, template_path : str, dest_path : str) -> None:    

    with open(from_path) as md_file:
        markdown = md_file.read()

    with open(template_path) as template_file:
        template = template_file.read()

    html_node = markdown_to_html_node(markdown)
    contents = html_node.to_html()
    page_title = extract_single_header(markdown)

    template = template.replace("{{ Content }}", contents)
    template = template.replace("{{ Title }}", page_title)

    dest_path = dest_path.replace('.md', '.html')
    with open(dest_path, "w") as file:
        file.write(template)


def generate_pages_recursive(dir_path_content : str, template_path : str, dest_dir_path : str) -> None:

    if not os.path.exists(dir_path_content):
        raise Exception("content directory not found")
    
    if not os.path.exists(template_path):
        raise Exception("html template file not found")
    
    print()
    print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}\n")

    if not os.path.isfile(dir_path_content):

        contents = os.listdir(dir_path_content)
        for elem in contents:
            if os.path.isfile(f"{dir_path_content}/{elem}") and f"{dir_path_content}/{elem}".endswith('.md'):
                generate_page(f"{dir_path_content}/{elem}", template_path, f"{dest_dir_path}/{elem}")
            else:
                os.mkdir(f"{dest_dir_path}/{elem}")
                generate_pages_recursive(f"{dir_path_content}/{elem}", template_path, f"{dest_dir_path}/{elem}")
    else:
        generate_page(dir_path_content, template_path, dest_dir_path)



