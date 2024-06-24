import textnode_utils
from textnode import TextNode, TextNodeType

def main():
    node = TextNode("Text with 2 consecutive *italic* *delimited parts*", TextNodeType.text)
    new_nodes = textnode_utils.split_nodes_delimiter([node], "*", TextNodeType.italic)
    print(new_nodes)

if __name__ == "__main__":
    main()