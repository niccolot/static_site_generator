import textnode_utils
from textnode import TextNode, TextNodeType
import re
import htmlnode_utils

def main():
    heading1 = "# a"
    heading2 = "## a"
    heading3 = "### a"
    heading4 = "#### a"
    heading5 = "##### a"
    heading6 = "###### a"

    code = "```a```"

    quote = "> a"

    unordered_list1 = "* a \n* b"
    unordered_list2 = "- a \n- b"

    ordered_list = "1. a \n2. b"
    paragraph = "a"

    heading_node1 = htmlnode_utils.heading_block_to_html_node(heading1)
    heading_node2 = htmlnode_utils.heading_block_to_html_node(heading2)
    heading_node3 = htmlnode_utils.heading_block_to_html_node(heading3)
    heading_node4 = htmlnode_utils.heading_block_to_html_node(heading4)
    heading_node5 = htmlnode_utils.heading_block_to_html_node(heading5)
    heading_node6 = htmlnode_utils.heading_block_to_html_node(heading6)

    code_node = htmlnode_utils.code_block_to_html_node(code)

    quote_node = htmlnode_utils.quote_block_to_html_node(quote)

    unordered_list_node1 = htmlnode_utils.unordered_list_block_to_html_node(unordered_list1)
    unordered_list_node2 = htmlnode_utils.unordered_list_block_to_html_node(unordered_list2)

    ordered_list_node = htmlnode_utils.ordered_list_block_to_html_node(ordered_list)

    paragraph_node = htmlnode_utils.paragraph_block_to_html_node(paragraph)

    print(unordered_list_node1)
    
if __name__ == "__main__":
    main()