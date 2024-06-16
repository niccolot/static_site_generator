from typing import Self, Type
from enum import Enum

from htmlnode import LeafNode

class TextNode:
    def __init__(self, text : str, text_type : str, url : str=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other_node : Self) -> bool:
        cond1 = self.text == other_node.text
        cond2 = self.text_type == other_node.text_type
        cond3 = self.url == other_node.url
        return cond1 and cond2 and cond3
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node : Type[TextNode]) -> Type[LeafNode]:
    TextNodeType = Enum('TextNodeType', ['text', 'bold', 'italic', 'code', 'link', 'image'])

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
