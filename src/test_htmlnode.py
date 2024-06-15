import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode()
        node2 = HTMLNode(tag="a", value="abcd", children=[node1], props={"href": "https://www.google.com", "target" : "_blank"})

        self.assertEqual("", node1.props_to_html())
        self.assertEqual(" href=\"https://www.google.com\" target=\"_blank\"", node2.props_to_html())

        repr_string1 = "(HTMLNode type)" + \
                        " tag: None" + \
                        " value: None" + \
                        " children: None" + \
                        " props: None"

        repr_string2 = "(HTMLNode type)" + \
                        " tag: a" + \
                        " value: abcd" + \
                        " children: [(HTMLNode type) tag: None value: None children: None props: None]" + \
                        " props: {'href': 'https://www.google.com', 'target': '_blank'}"
        
        self.assertEqual(repr_string1, node1.__repr__())
        self.assertEqual(repr_string2, node2.__repr__())


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        leaf1 = LeafNode(tag="p", value="This is a paragraph of text.")
        leaf2 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        leaf3 = LeafNode(value="just raw text")

        self.assertEqual("<p>This is a paragraph of text.</p>", leaf1.to_html())
        self.assertEqual("<a href=\"https://www.google.com\">Click me!</a>", leaf2.to_html())
        self.assertEqual("just raw text", leaf3.to_html())


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        parent1 = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
        )

        sub_parent = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text nested"),
                    LeafNode(None, "Normal text nested"),
                    LeafNode("i", "italic text nested"),
                    LeafNode(None, "Normal text nested"),
                ],
        )

        parent2 = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    sub_parent,
                    LeafNode(None, "Normal text"),
                ],
        )

        expected_string1 = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        expected_string2 = "<p><b>Bold text</b>Normal text" + \
                            "<p><b>Bold text nested</b>Normal text nested<i>italic text nested</i>Normal text nested</p>" + \
                            "Normal text</p>"

        self.assertEqual(expected_string1, parent1.to_html())
        self.assertEqual(expected_string2, parent2.to_html())


if __name__ == "__main__":
    unittest.main()
