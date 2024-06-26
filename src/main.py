import textnode_utils
from textnode import TextNode, TextNodeType
import re

def main():
    node = TextNode(
                "This is text with an ![image1]() and another ![image2](image2.png)",
                TextNodeType.text,
            )
        
    new_nodes = textnode_utils.split_nodes_image([node])
    print(new_nodes)
    
if __name__ == "__main__":
    main()