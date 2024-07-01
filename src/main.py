import textnode_utils
from textnode import TextNode, TextNodeType
import re

def main():
    with open("test_md.txt") as file:
        markdown = file.read()
        
    list = textnode_utils.markdown_to_blocks(markdown)
    print(list)
    
if __name__ == "__main__":
    main()