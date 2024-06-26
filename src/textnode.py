from typing import Self
from enum import Enum


TextNodeType = Enum('TextNodeType', ['text', 'bold', 'italic', 'code', 'link', 'image'])
MDBlockType = Enum('MDBlockType', ['paragraph', 'heading', 'code', 'quote', 'unordered_list', 'ordered_list'])


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


