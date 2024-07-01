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



def heading_block_to_html_node(block : str) -> Type[LeafNode]:

    if block_to_block_type(block) != MDBlockType.heading:
        raise Exception("Block of type different than 'heading' given, change block type or use appropriate function")
    
    heading_level = count_markdown_heading_level(block)
    value = block.lstrip('#').strip()
    tag = f"h{heading_level}"

    return LeafNode(tag, value)


def code_block_to_html_node(block : str) -> Type[ParentNode]:

    if block_to_block_type(block) != MDBlockType.code:
        raise Exception("Block of type different than 'code' given, change block type or use appropriate function")

    value = block.lstrip('```').rstrip('```').strip()
    pre_tag = "pre"
    code_tag = "code"

    leaf = LeafNode(code_tag, value)

    return ParentNode(pre_tag, [leaf])


def quote_block_to_html_node(block : str) -> Type[LeafNode]:

    if block_to_block_type(block) != MDBlockType.quote:
        raise Exception("Block of type different than 'quote' given, change block type or use appropriate function")

    value = block.lstrip('> ').strip()
    tag = "blockquote"

    return LeafNode(tag, value)


def unordered_list_block_to_html_node(block : str) -> Type[ParentNode]:

    if block_to_block_type(block) != MDBlockType.unordered_list:
        raise Exception("Block of type different than 'unordered list' given, change block type or use appropriate function")

    elements = parse_markdown_unordered_list(block)

    leafs = []

    for elem in elements:
        leafs.append(LeafNode("li", elem))
    
    return ParentNode("ul", leafs)


def ordered_list_block_to_html_node(block : str) -> Type[ParentNode]:
    
    if block_to_block_type(block) != MDBlockType.ordered_list:
        raise Exception("Block of type different than 'ordered list' given, change block type or use appropriate function")
    
    elements = parse_markdown_ordered_list(block)

    leafs = []

    for elem in elements:
        leafs.append(LeafNode("li", elem))
    
    return ParentNode("ol", leafs)


def paragraph_block_to_html_node(block : str) -> Type[LeafNode]:

    if block_to_block_type(block) != MDBlockType.paragraph:
        raise Exception("Block of type different than 'paragraph' given, change block type or use appropriate function")
    
    return LeafNode("p", block)


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
    nodes = []
    
    for block in blocks:
        
        type = block_to_block_type(block)
        converter = get_md_to_html_converter(type)
        nodes.append(converter(block))

    return ParentNode("div", nodes)