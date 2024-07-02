from typing import Type, Callable
import re

from htmlnode import LeafNode, ParentNode
from textnode_utils import *


def count_markdown_heading_level(heading: str) -> int:
    """
    Count the number of # characters at the beginning of a string to determine
    the level of a Markdown heading.
    """
    count = 0
    for char in heading:
        if char == '#':
            count += 1
        else:
            break
    return count


def parse_markdown_unordered_list(md_list: str) -> list[str]:
    """
    Parse a Markdown unordered list and return a list of elements with the 
    leading * or - characters stripped.
    """
    # Split the string by newlines to get each list item
    items = md_list.split('\n')
    # Strip the leading * or - and any surrounding whitespace from each item
    cleaned_items = [item.lstrip('*-').strip() for item in items if item.strip()]

    return cleaned_items


def parse_markdown_ordered_list(md_list: str) -> list[str]:
    """
    Parse a Markdown ordered list and return a list of elements with the 
    leading numbers and dots stripped.
    """
    
    # Split the string by newlines to get each list item
    items = md_list.split('\n')
    # Use regex to strip leading numbers and dots and any surrounding whitespace
    cleaned_items = [re.sub(r'^\d+\.\s*', '', item).strip() for item in items if item.strip()]

    return cleaned_items


def strip_quote_block(quote_block: str) -> str:
    # Split the block into lines
    lines = quote_block.split('\n')
    
    # Strip the "> " characters from each line
    stripped_lines = [line[2:].strip() if line.startswith('> ') else line.strip() for line in lines]
    
    # Join the stripped lines back into a single string
    cleaned_text = '\n'.join(stripped_lines).strip()
    
    return cleaned_text


def heading_block_to_html_node(block : str) -> Type[ParentNode]:

    if block_to_block_type(block) != MDBlockType.heading:
        raise Exception("Block of type different than 'heading' given, change block type or use appropriate function")
    
    heading_level = count_markdown_heading_level(block)
    text = block.lstrip('#').strip()
    outer_tag = f"h{heading_level}"

    text_nodes = text_to_textnode(text)
    leafs = []
    for node in text_nodes:
        leafs.append(text_node_to_html_node(node))

    return ParentNode(outer_tag, leafs)


def code_block_to_html_node(block : str) -> Type[ParentNode]:

    if block_to_block_type(block) != MDBlockType.code:
        raise Exception("Block of type different than 'code' given, change block type or use appropriate function")

    value = block.lstrip('```').rstrip('```').strip()
    pre_tag = "pre"
    code_tag = "code"

    leaf = LeafNode(code_tag, value)

    return ParentNode(pre_tag, [leaf])


def quote_block_to_html_node(block : str) -> Type[ParentNode]:
    
    if block_to_block_type(block) != MDBlockType.quote:
        raise Exception("Block of type different than 'quote' given, change block type or use appropriate function")

    #text = block.lstrip('> ').strip()
    text = strip_quote_block(block)
    outer_tag = "blockquote"

    text_nodes = text_to_textnode(text)
    leafs = []
    for node in text_nodes:
        leafs.append(text_node_to_html_node(node))

    return ParentNode(outer_tag, leafs)


def unordered_list_block_to_html_node(block : str) -> Type[ParentNode]:
    
    if block_to_block_type(block) != MDBlockType.unordered_list:
        raise Exception("Block of type different than 'unordered list' given, change block type or use appropriate function")

    md_elements = parse_markdown_unordered_list(block)

    parents = []
    html_elements_full_list = []

    for elem in md_elements:
        text_nodes = text_to_textnode(elem)
        html_elements_single_line = []

        for node in text_nodes:
            html_elements_single_line.append(text_node_to_html_node(node))

        html_elements_full_list.append(html_elements_single_line)

    for elem in html_elements_full_list:
        parents.append(ParentNode("li", elem))
    
    return ParentNode("ul", parents)
    
    
def ordered_list_block_to_html_node(block : str) -> Type[ParentNode]:

    if block_to_block_type(block) != MDBlockType.ordered_list:
        raise Exception("Block of type different than 'ordered list' given, change block type or use appropriate function")

    md_elements = parse_markdown_ordered_list(block)

    parents = []
    html_elements_full_list = []

    for elem in md_elements:
        text_nodes = text_to_textnode(elem)
        html_elements_single_line = []

        for node in text_nodes:
            html_elements_single_line.append(text_node_to_html_node(node))

        html_elements_full_list.append(html_elements_single_line)

    for elem in html_elements_full_list:
        parents.append(ParentNode("li", elem))
    
    return ParentNode("ol", parents)
    

def paragraph_block_to_html_node(block : str) -> Type[ParentNode]:
    
    if block_to_block_type(block) != MDBlockType.paragraph:
        raise Exception("Block of type different than 'paragraph' given, change block type or use appropriate function")
    
    text_nodes = text_to_textnode(block)
    
    leafs = []
    for node in text_nodes:
        if node.text != None:
            leafs.append(text_node_to_html_node(node))
    
    return ParentNode("p", leafs)
    
    
def get_md_to_html_converter(type : Type[MDBlockType]) -> Callable:

    if type == MDBlockType.heading:
        return heading_block_to_html_node
    
    elif type == MDBlockType.code:
        return code_block_to_html_node
    
    elif type == MDBlockType.quote:
        return quote_block_to_html_node
    
    elif type == MDBlockType.unordered_list:
        return unordered_list_block_to_html_node
    
    elif type == MDBlockType.ordered_list:
        return ordered_list_block_to_html_node
    
    elif type == MDBlockType.paragraph:
        return paragraph_block_to_html_node
    
    else:
        raise ValueError("Unrecognized markdown type")


def markdown_to_html_node(markdown : str) -> Type[ParentNode]:

    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    
    for block in blocks:
        
        type = block_to_block_type(block)
        converter = get_md_to_html_converter(type)
        block_nodes.append(converter(block))
        
    return ParentNode("div", block_nodes)