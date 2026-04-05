import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

def test_text_to_nodes(self):
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    self.assertEqual(text_to_textnodes(text), 
                    [
                        TextNode("This is ", TextType.TEXT),
                        TextNode("text", TextType.BOLD),
                        TextNode(" with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word and a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and an ", TextType.TEXT),
                        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", TextType.TEXT),
                        TextNode("link", TextType.LINK, "https://boot.dev"),
                    ]
                    )
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
class TestSplitNodes(unittest.TestCase):
    def test_code_valid(self):
        node = TextNode(text="This text has a `code example` followed by more text", text_type=TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], delimiter="`", text_type=TextType.CODE)
        self.assertListEqual(new_nodes, [TextNode(text="This text has a ", text_type=TextType.TEXT),
                              TextNode(text="code example", text_type=TextType.CODE),
                              TextNode(text=" followed by more text", text_type=TextType.TEXT)])



class TestExtract(unittest.TestCase):
    def test_extract_images(self):
       text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
       self.assertEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], extract_markdown_images(text))

    def test_extract_links(self):
       text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
       self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], extract_markdown_links(text))

class TestSplit(unittest.TestCase):
   def test_split_images(self):
      node = TextNode(
         "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
         TextType.TEXT,
      )
      new_nodes = split_nodes_image([node])
      self.assertListEqual(
         [
               TextNode("This is text with an ", TextType.TEXT),
               TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
               TextNode(" and another ", TextType.TEXT),
               TextNode(
                  "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
               ),
         ],
         new_nodes,
      )
   def test_split_links(self):
      node = TextNode(
            "This is text with a [first link](https://www.website1.com) and a [second link](https://www.website2.com)",
            TextType.TEXT,
         )
      new_nodes = split_nodes_link([node])
      self.assertListEqual(
            [
                  TextNode("This is text with a ", TextType.TEXT),
                  TextNode("first link", TextType.LINK, "https://www.website1.com"),
                  TextNode(" and a ", TextType.TEXT),
                  TextNode(
                     "second link", TextType.LINK, "https://www.website2.com"
                  ),
            ],
            new_nodes,
         )
      

if __name__ == "__main__":
    unittest.main()