from textnode_utils import *
from textnode import *
def main():
    node = TextNode(
            "This is text with an ![first image](image1.png) and another ![second image](image2.png)",
            TextNodeType.text,
        )

    new_nodes = split_nodes_image([node])
    print(new_nodes)


if __name__ == '__main__':
    main()