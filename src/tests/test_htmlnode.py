import unittest
import os

from site_generator.htmlnode import HTMLNode, LeafNode, ParentNode
from site_generator import htmlnode_utils


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

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
        leaf4 = LeafNode()

        self.assertEqual("<p>This is a paragraph of text.</p>", leaf1.to_html())
        self.assertEqual("<a href=\"https://www.google.com\">Click me!</a>", leaf2.to_html())
        self.assertEqual("just raw text", leaf3.to_html())
        with self.assertRaises(ValueError):
            leaf4.to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        # normal case
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
        # nesteed case
        parent2 = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    sub_parent,
                    LeafNode(None, "Normal text"),
                ],
        )
        # invalid case (no tag)
        parent3 = ParentNode(
                tag=None,
                children=[
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    sub_parent,
                    LeafNode(None, "Normal text"),
                ],
        )
        # invalid case (no children)
        parent4 = ParentNode(
                "p",
                children=None
        )

        expected_string1 = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        expected_string2 = "<p><b>Bold text</b>Normal text" + \
                            "<p><b>Bold text nested</b>Normal text nested<i>italic text nested</i>Normal text nested</p>" + \
                            "Normal text</p>"

        self.assertEqual(expected_string1, parent1.to_html())
        self.assertEqual(expected_string2, parent2.to_html())
        with self.assertRaises(ValueError):
            parent3.to_html()
            parent4.to_html()


class TestHTMLNodeUtils(unittest.TestCase):
    def test_blocks_to_html(self):

        heading1 = "# a"
        heading2 = "## a"
        heading3 = "### a"
        heading4 = "#### a"
        heading5 = "##### a"
        heading6 = "###### a"

        code = "```a```"

        quote = "> a"

        unordered_list1 = "* a \n* b"
        unordered_list2 = "- a \n- b"

        ordered_list = "1. a \n2. b"
        paragraph = "a"

        heading_node1 = htmlnode_utils.heading_block_to_html_node(heading1)
        heading_node2 = htmlnode_utils.heading_block_to_html_node(heading2)
        heading_node3 = htmlnode_utils.heading_block_to_html_node(heading3)
        heading_node4 = htmlnode_utils.heading_block_to_html_node(heading4)
        heading_node5 = htmlnode_utils.heading_block_to_html_node(heading5)
        heading_node6 = htmlnode_utils.heading_block_to_html_node(heading6)

        code_node = htmlnode_utils.code_block_to_html_node(code)

        quote_node = htmlnode_utils.quote_block_to_html_node(quote)

        unordered_list_node1 = htmlnode_utils.unordered_list_block_to_html_node(unordered_list1)
        unordered_list_node2 = htmlnode_utils.unordered_list_block_to_html_node(unordered_list2)

        ordered_list_node = htmlnode_utils.ordered_list_block_to_html_node(ordered_list)

        paragraph_node = htmlnode_utils.paragraph_block_to_html_node(paragraph)

        self.assertEqual("<h1>a</h1>", heading_node1.to_html())
        self.assertEqual("<h2>a</h2>", heading_node2.to_html())
        self.assertEqual("<h3>a</h3>", heading_node3.to_html())
        self.assertEqual("<h4>a</h4>", heading_node4.to_html())
        self.assertEqual("<h5>a</h5>", heading_node5.to_html())
        self.assertEqual("<h6>a</h6>", heading_node6.to_html())

        self.assertEqual("<pre><code>a</code></pre>", code_node.to_html())

        self.assertEqual("<blockquote>a</blockquote>", quote_node.to_html())

        self.assertEqual("<ul><li>a</li><li>b</li></ul>", unordered_list_node1.to_html())
        self.assertEqual("<ul><li>a</li><li>b</li></ul>", unordered_list_node2.to_html())

        self.assertEqual("<ol><li>a</li><li>b</li></ol>", ordered_list_node.to_html())

        self.assertEqual("<p>a</p>", paragraph_node.to_html())

    
    def test_markdown_to_html_node(self):

        asset_path = os.path.join(os.path.dirname(__file__), 'assets', 'test_md2.txt')
        
        with open(asset_path) as file:
            markdown = file.read()

        html_node = htmlnode_utils.markdown_to_html_node(markdown)

        expected_html = (
                            "<div>"
                            "<h1>a</h1>"
                            "<pre><code>a</code></pre>"
                            "<blockquote>a</blockquote>"
                            "<ul>"
                            "<li>a</li>"
                            "<li>b</li>"
                            "</ul>"
                            "<ul>"
                            "<li>a</li>"
                            "<li>b</li>"
                            "</ul>"
                            "<ol>"
                            "<li>a</li>"
                            "<li>b</li>"
                            "</ol>"
                            "<p>a</p>"
                            "</div>"
                        )
        
        self.assertEqual(expected_html, html_node.to_html())

if __name__ == "__main__":
    unittest.main()
