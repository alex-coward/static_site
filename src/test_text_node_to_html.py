import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from text_node_to_html_node import text_node_to_html_node

class Test_text_node_to_html_node(unittest.TestCase):
    def test_TextType_TEXT(self):
        node = TextNode(text="This is a text node", text_type=TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node, LeafNode(tag=None, value="This is a text node"))
    
    def test_TextType_BOLD(self):
        node = TextNode(text="This is a text node", text_type=TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node, LeafNode(tag="b", value="This is a text node"))

    def test_TextType_ITALIC(self):
        node = TextNode(text="This is a text node", text_type=TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node, LeafNode(tag="i", value="This is a text node"))

    def test_TextType_CODE(self):
        node = TextNode(text="This is a text node", text_type=TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node, LeafNode(tag="code", value="This is a text node"))
    
    def test_TextType_LINK(self):
        node = TextNode(text="This is Google.com", text_type=TextType.LINK, url="www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node, LeafNode(tag="a", value="This is Google.com", props={"href": "www.google.com"}))
    
    def test_TextType_IMAGE(self):
        node = TextNode(text="This is a cat", text_type=TextType.IMAGE, url="www.cutecat.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node, LeafNode(tag="img", value="",  props={"src": "www.cutecat.com" , "alt": "This is a cat"}))
    