import textnode_utils


def main():
    text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
    print(textnode_utils.extract_markdown_links(text))

if __name__ == "__main__":
    main()