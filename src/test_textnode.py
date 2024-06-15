import unittest

from textnode import TextNode


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

if __name__ == "__main__":
    unittest.main()