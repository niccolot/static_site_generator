from typing import Type
import re
import warnings 

from htmlnode import LeafNode
from textnode import TextNodeType, TextNode, MDBlockType


def text_node_to_html_node(text_node : Type[TextNode]) -> Type[LeafNode]:

    if text_node.text_type == TextNodeType.text:
        return LeafNode(None, text_node.text, None)
    
    elif text_node.text_type == TextNodeType.bold:
        return LeafNode("b", text_node.text, None)
    
    elif text_node.text_type == TextNodeType.italic:
        return LeafNode("i", text_node.text, None)
    
    elif text_node.text_type == TextNodeType.code:
        return LeafNode("code", text_node.text, None)
    
    elif text_node.text_type == TextNodeType.link:
        return LeafNode("a", text_node.text, {"href" : f"{text_node.url}"})
    
    elif text_node.text_type == TextNodeType.image:
        props = {
            "src" : text_node.url,
            "alt" : text_node.text
        }
        return LeafNode("img", None, props)
    
    raise Exception('Invalid text node type')


def is_valid_markdown(text : str, delimiter : str) -> bool:
    if delimiter not in text:
        return True
    
    delimiter_count = text.count(delimiter)
    return delimiter_count % 2 == 0


def check_delimiter_validity(delimiter : str) -> bool:
    if delimiter == "`":
        return True
    
    elif delimiter == "*":
        return True
    
    elif delimiter == "**":
        return True
    
    else:
        return False
    

def split_markdown_inline(text : str, delimiter : str) -> list[str]:
    """
    ensures that bold and italic text are splitted correctly

    text1 = "aaa **bbb** ccc"
    text2 = "aaa *bbb* ccc"

    # Splitting with "**" delimiter
    print(split_markdown(text1, "**"))  # Output: ['aaa ', 'bbb', ' ccc']

    # Splitting with "*" delimiter
    print(split_markdown(text2, "*"))  # Output: ['aaa ', 'bbb', ' ccc']

    # Splitting with "*" on text with "**"
    print(split_markdown(text1, "*"))  # Output: ['aaa **bbb** ccc']
    """

    # code text is easy to split 
    if delimiter == "`":
        return text.split(delimiter)
    else:
        # Escape the delimiter for regex
        escaped_delimiter = re.escape(delimiter)
        # Find all positions of the standalone delimiter
        matches = list(re.finditer(r'(?<!\*)' + escaped_delimiter + r'(?!\*)', text))
        
        if not matches:
            return [text]
        
        parts = []
        last_end = 0
        
        for match in matches:
            start, end = match.span()
            parts.append(text[last_end:start])
            last_end = end
            
        parts.append(text[last_end:])
        return parts


def split_nodes_delimiter(old_nodes : list[TextNode], delimiter : str, text_type : Type[TextNodeType]) -> list[TextNode]:
    """
    given list of TextNode with just text it separates the text parts from the bold italic or code parts e.g.

    node = TextNode("This is text with a `code block` word", TextNodeType.text)
    new_nodes = split_nodes_delimiter([node1], "`", TextNodeType.code)

    new_nodes == [
                        TextNode("This is text with a ", TextNodeType.text),
                        TextNode("code block", TextNodeType.code),
                        TextNode(" word", TextNodeType.text),
                    ]

    same thing with bold or italic
    """
    
    if not check_delimiter_validity(delimiter):
        raise Exception("Invalid delimiter")
    
    def split_single_node(node : Type[TextNode], delimiter : str, text_type : Type[TextNodeType]) -> list[TextNode]:
        ret_list = []
        text = node.text
        old_type = node.text_type

        if not is_valid_markdown(text, delimiter):
            raise Exception(f"Invalid markdown delimiter syntax: matching {delimiter} character not found")
        else: 
            #text_list = text.split(f"{delimiter}")
            text_list = split_markdown_inline(text, delimiter)
            for i in range(len(text_list)):
                # in a valid string the text enclosed by the delimiters (code, italic or bold) will be located on odd indexes 
                # e.g. str_a = "*a*bcd*ef*" -> str_a.split("*") == ['', 'a', 'bcd', 'ef', ''] 
                # str_b = "a*b*cd*ef*" -> str_b.split("*") == ['a', 'b', 'cd', 'ef', '']
                # str_c = "*a* *ef*" -> str_c.split("*") == ['', 'a', ' ', 'ef', '']
                if i % 2 != 0: 
                    new_node = TextNode(text_list[i], text_type, node.url)
                    ret_list.append(new_node)
                else:
                    new_node = TextNode(text_list[i], old_type, node.url)
                    ret_list.append(new_node)
        
        # filter out empty text resulting from the splitting of a string with 
        # a delimited part at the end, like str_b or str_c in the comment above
        filtered_ret_list = [node for node in ret_list if node.text != ""]
        
        return filtered_ret_list

    ret_list = []
    for node in old_nodes:
        if (node.text_type is not TextNodeType.text) and (node.text_type is not TextNodeType.code):
            ret_list.append(node)
        else:
            ret_list.extend(split_single_node(node, delimiter, text_type))
    
    return ret_list


def split_nodes_image(old_nodes : list[TextNode]) -> list[TextNode]:
    """
    given a list of TextNode with just text it separates the images part e.g.

    node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextNodeType.text,
        )

    new_nodes = split_nodes_image([node])

    new_nodes == [
                    TextNode("This is text with an ", text_type_text),
                    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and another ", text_type_text),
                    TextNode(
                        "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                    ),
                ]
    """
    def split_single_node_image(node : Type[TextNode]) -> list[TextNode]:
        ret_list = []
        text = node.text
        old_type = node.text_type
        old_url = node.url
        text_list, alt_text_idxs = split_markdown_imgs_links_with_indices(text, img=True)

        i = 0
        while i < len(text_list):
            if i in alt_text_idxs:
                alt_text = text_list[i]
                url = text_list[i+1]
                new_node = TextNode(alt_text, TextNodeType.image, url)
                ret_list.append(new_node)
                i += 1
            else:
                new_node = TextNode(text_list[i], old_type, old_url)
                ret_list.append(new_node)
            
            i += 1
        
        return ret_list
    
    ret_list = []
    for node in old_nodes:
        ret_list.extend(split_single_node_image(node))

    ret_list = [node for node in ret_list if node.text != '']
    
    return ret_list


def split_nodes_link(old_nodes : list[TextNode]) -> list[TextNode]:
    """
    same usage as split_nodes_image but with links
    """
    def split_single_node_link(node : Type[TextNode]) -> list[TextNode]:
        ret_list = []
        text = node.text
        old_type = node.text_type
        old_url = node.url
        text_list, alt_text_idx = split_markdown_imgs_links_with_indices(text, img=False)

        i = 0
        while i < len(text_list):
            if i in alt_text_idx:
                alt_text = text_list[i]
                url = text_list[i+1]
                new_node = TextNode(alt_text, TextNodeType.link, url)
                ret_list.append(new_node)
                i += 1
            else:
                new_node = TextNode(text_list[i], old_type, old_url)
                ret_list.append(new_node)
            
            i += 1
        
        return ret_list
    
    ret_list = []
    for node in old_nodes:
        ret_list.extend(split_single_node_link(node))

    ret_list = [node for node in ret_list if node.text != '']
    
    return ret_list


def split_markdown_imgs_links_with_indices(text : str, img : bool) -> tuple[list[str], list[int]]:

    if img:
        # Regex pattern to match the image markdown
        # pattern1 is to obtain a splitting e.g.
        # "This is text with an ![image1](image1.png) and another ![image2](image2.png)" -> ['This is text with an ', '![image1](image1.png)', ' and another ', '![image2](image2.png)']
        #
        # pattern2 is used to strip alt_text and url of parenthesis and separate them e.g.
        # ![image1](image1.png) -> (image1, image1.png) in order to be extracted separately later
        pattern1 = r'(\!\[.*?\]\(.*?\))'  
        pattern2 = r'\!\[(.*?)\]\((.*?)\)'
    else:
        # Regex pattern to match the link markdown
        # same concepts as with images
        pattern1 = r'((?<!\!)\[.*?\]\(.*?\))'
        pattern2 = r'(?<!\!)\[(.*?)\]\((.*?)\)'
    
    # Split the text by the image markdown pattern
    parts = re.split(pattern1, text)
    
    result = []
    alt_text_indices = []
    
    for part in parts:
        if re.match(pattern1, part):
            # Extract the alt text and image link
            alt_text, url = re.findall(pattern2, part)[0]

            # if no image or link content given, warn the user and do not append anything
            if not url:
                warnings.warn("Markdown syntax detected but no content given", UserWarning)
                continue

            result.append(alt_text)
            result.append(url)
            alt_text_indices.append(len(result) - 2)  # Store the index of the alt text element
        else:
            result.append(part)
    
    return result, alt_text_indices

        

def extract_markdown_images(text : str) -> list[tuple]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text : str) -> list[tuple]:
    matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return matches


def text_to_textnode(text : str) -> list[TextNode]:
    
    node = TextNode(text, TextNodeType.text)
    x = split_nodes_delimiter([node], "*", TextNodeType.italic)
    x = split_nodes_delimiter(x, "**", TextNodeType.bold)
    x = split_nodes_delimiter(x, "`", TextNodeType.code)
    x = split_nodes_link(x)
    x = split_nodes_image(x)

    return x


def markdown_to_blocks(markdown : str) -> list[str]:
    # Use regex to split the markdown string by \n\n
    blocks = re.split(r'\n\s*\n', markdown)
    
    # Strip leading and trailing whitespace from each block and filter out any empty blocks
    processed_blocks = [block.strip() for block in blocks if block.strip()]
    
    return processed_blocks


def block_to_block_type(block : str) -> MDBlockType:

    if re.match(r'#{1,6} ', block):
        return MDBlockType.heading
    
    if block.startswith('```') and block.endswith('```'):
        return MDBlockType.code
    
    if all(line.startswith('> ') for line in block.split('\n')):
        return MDBlockType.quote
    
    if all(line.startswith(('* ', '- ')) for line in block.split('\n')):
        return MDBlockType.unordered_list
    
    ordered_list_pattern = r'^(\d+)\. '
    lines = block.split('\n')
    if all(re.match(ordered_list_pattern, line) for line in lines):
        # Check if numbers increment by 1
        numbers = [int(re.match(ordered_list_pattern, line).group(1)) for line in lines]
        if numbers == list(range(1, len(lines) + 1)):
            return MDBlockType.ordered_list
    
    
    return MDBlockType.paragraph

