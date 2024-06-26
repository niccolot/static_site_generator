import unittest

from textnode import TextNode, TextNodeType
import textnode_utils


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


class TestTextNodeUtils(unittest.TestCase):

    def test_split_nodes_delimiter(self):

        node1 = TextNode("This is text with a `code block` word", TextNodeType.text)
        new_nodes1 = textnode_utils.split_nodes_delimiter([node1], "`", TextNodeType.code)

        expected_nodes1 = [
                            TextNode("This is text with a ", TextNodeType.text),
                            TextNode("code block", TextNodeType.code),
                            TextNode(" word", TextNodeType.text),
                        ]
        
        node2 = TextNode("This is a different text with more `code` inside", TextNodeType.text)
        new_nodes2 = textnode_utils.split_nodes_delimiter([node1, node2], "`", TextNodeType.code)

        expected_nodes2 = [
                            TextNode("This is text with a ", TextNodeType.text),
                            TextNode("code block", TextNodeType.code),
                            TextNode(" word", TextNodeType.text),
                            TextNode("This is a different text with more ", TextNodeType.text),
                            TextNode("code", TextNodeType.code),
                            TextNode(" inside", TextNodeType.text),
                        ]
        
        node3 = TextNode("This is another different text but with **bold** text inside", TextNodeType.text)
        new_nodes3 = textnode_utils.split_nodes_delimiter([node1, node2, node3], "`", TextNodeType.code)

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
        new_nodes4 = textnode_utils.split_nodes_delimiter([node4], "**", TextNodeType.bold)

        expected_nodes4 = [
                            TextNode("This is text with a ", TextNodeType.text),
                            TextNode("bold", TextNodeType.bold),
                            TextNode(" word", TextNodeType.text),
                        ]
        
        node5 = TextNode("This is text with a *italic* word", TextNodeType.text)
        new_nodes5 = textnode_utils.split_nodes_delimiter([node5], "*", TextNodeType.italic)

        expected_nodes5 = [
                            TextNode("This is text with a ", TextNodeType.text),
                            TextNode("italic", TextNodeType.italic),
                            TextNode(" word", TextNodeType.text),
                        ]
        
        single_delimiter_node = TextNode("This is text with an *unclosed delimiter", TextNodeType.text)

        node6 = TextNode("Text with 2 consecutive *italic* *delimited parts*", TextNodeType.text)
        node7 = TextNode("Text with 2 consecutive **bold** **delimited parts**", TextNodeType.text)
        node8 = TextNode("Text with 2 consecutive `code` `delimited parts`", TextNodeType.text)

        new_nodes6 = textnode_utils.split_nodes_delimiter([node6], "*", TextNodeType.italic)
        new_nodes7 = textnode_utils.split_nodes_delimiter([node7], "**", TextNodeType.bold)
        new_nodes8 = textnode_utils.split_nodes_delimiter([node8], "`", TextNodeType.code)

        expected_nodes6 = [
                            TextNode("Text with 2 consecutive ", TextNodeType.text),
                            TextNode("italic", TextNodeType.italic),
                            TextNode(" ", TextNodeType.text),
                            TextNode("delimited parts", TextNodeType.italic),
                        ]
        
        expected_nodes7 = [
                            TextNode("Text with 2 consecutive ", TextNodeType.text),
                            TextNode("bold", TextNodeType.bold),
                            TextNode(" ", TextNodeType.text),
                            TextNode("delimited parts", TextNodeType.bold),
                        ]
        
        expected_nodes8 = [
                            TextNode("Text with 2 consecutive ", TextNodeType.text),
                            TextNode("code", TextNodeType.code),
                            TextNode(" ", TextNodeType.text),
                            TextNode("delimited parts", TextNodeType.code),
                        ]

        self.assertListEqual(new_nodes1, expected_nodes1)
        self.assertListEqual(new_nodes2, expected_nodes2)
        self.assertListEqual(new_nodes3, expected_nodes3)
        self.assertListEqual(new_nodes4, expected_nodes4)
        self.assertListEqual(new_nodes5, expected_nodes5)
        self.assertListEqual(new_nodes6, expected_nodes6)
        self.assertListEqual(new_nodes7, expected_nodes7)
        self.assertListEqual(new_nodes8, expected_nodes8)

        with self.assertRaises(Exception) as e:
            _ = textnode_utils.split_nodes_delimiter([node5], "!", TextNodeType.italic)
            self.assertEqual(str(e.exception), "Invalid delimiter")

        with self.assertRaises(Exception) as e:   
            _ = textnode_utils.split_nodes_delimiter([single_delimiter_node], "*", TextNodeType.italic)
            self.assertEqual(str(e.exception), "Invalid markdown delimiter syntax: matching * character not found")


    def test_extract_markdown_image_link(self):

        text_with_images =  "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        text_with_links = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        text_with_nothing = "This is a text without images or links"
        image_with_no_contents = "This is a text with an empty image ![image]()"
        link_with_no_contents = "This is a text with an empty link [link]()"
        text_with_both =  text_with_images + text_with_links

        images_list = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        links_list = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        nothing_list = []
        no_image_list = [("image", "")]
        no_link_list = [("link", "")]

        self.assertListEqual(images_list, textnode_utils.extract_markdown_images(text_with_images))
        self.assertListEqual(links_list, textnode_utils.extract_markdown_links(text_with_links))
        self.assertListEqual(images_list, textnode_utils.extract_markdown_images(text_with_both))
        self.assertListEqual(links_list, textnode_utils.extract_markdown_links(text_with_both))
        self.assertListEqual(nothing_list, textnode_utils.extract_markdown_images(text_with_nothing))
        self.assertListEqual(nothing_list, textnode_utils.extract_markdown_links(text_with_nothing))
        self.assertListEqual(no_image_list, textnode_utils.extract_markdown_images(image_with_no_contents))
        self.assertListEqual(no_link_list, textnode_utils.extract_markdown_links(link_with_no_contents))

    
    def test_split_nodes_image(self):

        node1 = TextNode(
                "This is text with an ![image1](image1.png) and another ![image2](image2.png)",
                TextNodeType.text,
            )
        
        new_nodes1 = textnode_utils.split_nodes_image([node1])

        expected_nodes1 = [
                            TextNode("This is text with an ", TextNodeType.text),
                            TextNode("image1", TextNodeType.image, "image1.png"),
                            TextNode(" and another ", TextNodeType.text),
                            TextNode("image2", TextNodeType.image, "image2.png"),
                        ]
        
        self.assertListEqual(new_nodes1, expected_nodes1)

if __name__ == "__main__":
    unittest.main()