import textnode_utils
from textnode import TextNode, TextNodeType
import re

def main():
    text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
    nodes = textnode_utils.text_to_textnode(text)
    print(nodes)
    
if __name__ == "__main__":
    main()