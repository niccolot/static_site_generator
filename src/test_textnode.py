import unittest

from textnode import TextNode, split_nodes_delimiter, TextNodeType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        node3 = TextNode("This is a node with different text but same text type", "bold")
        node4 = TextNode("This is a text node", "italic")
        node5 = TextNode("This is a text node", "italic", "https:pippo")
        node6 = TextNode("This is a text node", "italic", "https:pippo2")
        node7 = TextNode("This is a text node", "italic", "https:pippo2")

        self.assertEqual(node, node2) # same text, same text type, same url==None
        self.assertNotEqual(node2, node3) # different text, same text type, same url==None
        self.assertNotEqual(node2, node4) # same text, different text type, same url==None
        self.assertNotEqual(node4, node5) # same text, same text type, different url with one as None
        self.assertNotEqual(node5, node6) # same text, same text type, different url
        self.assertEqual(node6, node7) # same text, same text type, same url


class TextSplitNodesDelimiter(unittest.TestCase):
    def test(self):
        node1 = TextNode("This is text with a `code block` word", TextNodeType.text)
        new_nodes1 = split_nodes_delimiter([node1], "`", TextNodeType.code)

        expected_nodes1 = [
                            TextNode("This is text with a ", TextNodeType.text),
                            TextNode("code block", TextNodeType.code),
                            TextNode(" word", TextNodeType.text),
                        ]
        
        node2 = TextNode("This is a different text with more `code` inside", TextNodeType.text)
        new_nodes2 = split_nodes_delimiter([node1, node2], "`", TextNodeType.code)

        expected_nodes2 = [
                            TextNode("This is text with a ", TextNodeType.text),
                            TextNode("code block", TextNodeType.code),
                            TextNode(" word", TextNodeType.text),
                            TextNode("This is a different text with more ", TextNodeType.text),
                            TextNode("code", TextNodeType.code),
                            TextNode(" inside", TextNodeType.text),
                        ]
        
        node3 = TextNode("This is another different text but with **bold** text inside", TextNodeType.text)
        new_nodes3 = split_nodes_delimiter([node1, node2, node3], "`", TextNodeType.code)

        expected_nodes3 = [
                            TextNode("This is text with a ", TextNodeType.text),
                            TextNode("code block", TextNodeType.code),
                            TextNode(" word", TextNodeType.text),
                            TextNode("This is a different text with more ", TextNodeType.text),
                            TextNode("code", TextNodeType.code),
                            TextNode(" inside", TextNodeType.text),
                            TextNode("This is another different text but with **bold** text inside", TextNodeType.text)
                        ]
        
        node4 = TextNode("This is text with a **bold** word", TextNodeType.text)
        new_nodes4 = split_nodes_delimiter([node4], "**", TextNodeType.bold)

        expected_nodes4 = [
                            TextNode("This is text with a ", TextNodeType.text),
                            TextNode("bold", TextNodeType.bold),
                            TextNode(" word", TextNodeType.text),
                        ]
        
        node5 = TextNode("This is text with a *italic* word", TextNodeType.text)
        new_nodes5 = split_nodes_delimiter([node5], "*", TextNodeType.italic)

        expected_nodes5 = [
                            TextNode("This is text with a ", TextNodeType.text),
                            TextNode("italic", TextNodeType.italic),
                            TextNode(" word", TextNodeType.text),
                        ]
        
        single_delimiter_node = TextNode("This is text with an *unclosed delimiter", TextNodeType.text)

        self.assertListEqual(new_nodes1, expected_nodes1)
        self.assertListEqual(new_nodes2, expected_nodes2)
        self.assertListEqual(new_nodes3, expected_nodes3)
        self.assertListEqual(new_nodes4, expected_nodes4)
        self.assertListEqual(new_nodes5, expected_nodes5)

        with self.assertRaises(Exception) as e:
            _ = split_nodes_delimiter([node5], "!", TextNodeType.italic)
            self.assertEqual(str(e.exception), "Invalid delimiter")

        with self.assertRaises(Exception) as e:   
            _ = split_nodes_delimiter([single_delimiter_node], "*", TextNodeType.italic)
            self.assertEqual(str(e.exception), "Invalid markdown delimiter syntax: matching * character not found")


if __name__ == "__main__":
    unittest.main()