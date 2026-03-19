import unittest
from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter


class TestSplitNodes(unittest.TestCase):
    def test_code_valid(self):
        node = TextNode(text="This text has a `code example` followed by more text", text_type=TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], delimiter="`", text_type=TextType.CODE)
        self.assertListEqual(new_nodes, [TextNode(text="This text has a ", text_type=TextType.TEXT),
                              TextNode(text="code example", text_type=TextType.CODE),
                              TextNode(text=" followed by more text", text_type=TextType.TEXT)])

if __name__ == "__main__":
    unittest.main()