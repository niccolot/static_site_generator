from typing import Type
import re
import warnings 

from htmlnode import LeafNode
from textnode import TextNodeType, TextNode


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
        if not is_valid_markdown(text, delimiter):
            raise Exception(f"Invalid markdown delimiter syntax: matching {delimiter} character not found")
        else: 
            text_list = text.split(f"{delimiter}")
            for i in range(len(text_list)):
                # in a valid string the text enclosed by the delimiters (code, italic or bold) will be located on odd indexes 
                # e.g. str_a = "*a*bcd*ef*" -> str_a.split("*") == ['', 'a', 'bcd', 'ef', ''] 
                # str_b = "a*b*cd*ef*" -> str_b.split("*") == ['a', 'b', 'cd', 'ef', '']
                # str_c = "*a* *ef*" -> str_c.split("*") == ['', 'a', ' ', 'ef', '']
                if i % 2 != 0: 
                    new_node = TextNode(text_list[i], text_type, node.url)
                    ret_list.append(new_node)
                else:
                    new_node = TextNode(text_list[i], TextNodeType.text, node.url)
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
            text_type_text,
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
        text_list, image_parts_idxs = split_markdown_imgs_links_with_indices(text, img=True)

        for i in range(len(text_list)):
            if i in image_parts_idxs:
                alt_text_and_url = text_list[i].split()
                new_node = TextNode(alt_text_and_url[0], TextNodeType.image, alt_text_and_url[1])
                ret_list.append(new_node)
            else:
                new_node = TextNode(text_list[i], TextNodeType.text)
                ret_list.append(new_node)
        
        return ret_list
    
    ret_list = []
    for node in old_nodes:
        ret_list.extend(split_single_node_image(node))
    
    return ret_list


def split_nodes_link(old_nodes : list[TextNode]) -> list[TextNode]:
    """
    same usage as split_nodes_image but with links
    """
    def split_single_node_link(node : Type[TextNode]) -> list[TextNode]:
        ret_list = []
        text = node.text
        text_list, image_parts_idxs = split_markdown_imgs_links_with_indices(text, img=False)

        for i in range(len(text_list)):
            if i in image_parts_idxs:
                alt_text_and_url = text_list[i].split()
                new_node = TextNode(alt_text_and_url[0], TextNodeType.link, alt_text_and_url[1])
                ret_list.append(new_node)
            else:
                new_node = TextNode(text_list[i], TextNodeType.text)
                ret_list.append(new_node)
        
        return ret_list
    
    ret_list = []
    for node in old_nodes:
        ret_list.extend(split_single_node_link(node))
    
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
    
    # Split the text by the image or link markdown pattern
    parts = re.split(pattern1, text)
    # filter out empty text
    parts = [part for part in parts if part]
    
    result = []
    indices = []
    
    for part in parts:
        if re.match(pattern1, part):
            # Extract the alt text and image link url
            alt_text, url = re.findall(pattern2, part)[0] # extract first (and only) match, otherwise it would be a list and not the tuple inside the list

            # if no image or link content given, warn the user and do not append anything
            if not url:
                warnings.warn("Markdown syntax detected but no content given", UserWarning)
                continue
            
            result.append(f"{alt_text} {url}")
            indices.append(len(result) - 1)  # Store the index of the image or link element
        else:
            result.append(part)
    
    return result, indices
        

def extract_markdown_images(text : str) -> list[tuple]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text : str) -> list[tuple]:
    matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return matches


def text_to_textnode(text : str) -> list[TextNode]:
    
    
    node = TextNode(text, TextNodeType.text)
    print(node)
    print()
    """
    x = split_nodes_delimiter([node], "*", TextNodeType.italic)
    print(x)
    print()
    x = split_nodes_delimiter(x, "**", TextNodeType.bold)
    print(x)
    print()
    x = split_nodes_delimiter(x, "`", TextNodeType.code)
    print(x)
    print()
    x = split_nodes_image(x)
    print(x)
    print()
    x = split_nodes_link(x)
    """
    x = split_nodes_image([node])
    return x