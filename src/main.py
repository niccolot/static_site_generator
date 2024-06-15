from textnode import TextNode

def main():
    node1 = TextNode("This is a text node", "bold", "https://www.boot.dev")
    node2 = TextNode("This is a different node", "bold", "https://www.boot.dev")
    node3 = TextNode("This is a text node", "bold", "https://www.boot.dev")

    print(node1)
    print(node2)
    print(node3)

    print(node1 == node2)
    print(node1 == node3)

if __name__ == "__main__":
    main()