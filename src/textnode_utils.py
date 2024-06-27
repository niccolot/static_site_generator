from typing import Self, Type
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


def split_nodes_delimiter(old_nodes : list[Self], delimiter : str, text_type : Type[TextNodeType]) -> list[TextNode]:
    
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


def split_nodes_image(old_nodes : list[Self]) -> list[TextNode]:
    def split_single_node_image(node : Type[TextNode]) -> list[TextNode]:
        ret_list = []
        text = node.text
        text_list, image_parts_idxs = split_markdown_images_with_indices(text)

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


def split_markdown_images_with_indices(text : str) -> tuple[list[str], list[int]]:
    # Regex pattern to match the image markdown
    pattern = r'(\!\[.*?\]\(.*?\))'
    
    # Split the text by the image markdown pattern
    parts = re.split(pattern, text)
    parts = [part for part in parts if part]
    
    result = []
    image_indices = []
    
    for part in parts:
        if re.match(pattern, part):
            # Extract the alt text and image link
            alt_text, image_link = re.findall(r'\!\[(.*?)\]\((.*?)\)', part)[0]

            # if no image content given, warn the user and do not append anything
            if not image_link:
                warnings.warn("Markdown syntax detected but no content given", UserWarning)
                continue
            
            result.append(f"{alt_text} {image_link}")
            image_indices.append(len(result) - 1)  # Store the index of the image element
        else:
            result.append(part)
    
    return result, image_indices
        

def extract_markdown_images(text : str) -> list[tuple]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text : str) -> list[tuple]:
    matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return matches