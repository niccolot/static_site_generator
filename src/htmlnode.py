from typing import Self

class HTMLNode:
    def __init__(self, 
                 tag : str = None, 
                 value : str = None, 
                 children : list[Self] = None, 
                 props : dict = None
        ) -> None:
        
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> None:
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        props = ""
        if self.props:
            for k,v in self.props.items():
                props += f" {k}=\"{v}\""

        return props

    def __repr__(self) -> str:
        return f"(HTMLNode type) tag: {self.tag} value: {self.value} children: {self.children} props: {self.props}"
    

class LeafNode(HTMLNode):
    def __init__(self, 
                 tag : str = None, 
                 value : str = None, 
                 props : dict = None
        ) -> None:

        super().__init__(tag, value, None, props)
        
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Value of LeafNode must be not None")
        
        # not tag -> raw text
        if self.tag is None:
            return f"{self.value}"

        # tag and properties
        if self.props is not None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
        # just tag
        return f"<{self.tag}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, 
                tag : str, 
                children : list[Self], 
                props : dict = None
        ) -> None:

        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag == None:
           raise ValueError("'tag' argument must be provided")
        if self.children == None:
           raise ValueError("'children' argument must be provided")

        out_string = f"<{self.tag}>"
        for child_node in self.children:
           out_string += child_node.to_html()
        
        out_string += f"</{self.tag}>"
        
        return out_string