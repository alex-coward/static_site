import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_HTMLNode_repr(self):
        node = HTMLNode(tag=None, value="one", children=["done"], props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.__repr__(), f"HTMLNode({node.tag}, {node.value}, {node.children}, {node.props})" )

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.funkymonkey.com", "target": "banana"})
        self.assertEqual(node.props_to_html(), " href=https://www.funkymonkey.com target=banana")

    def test_empty_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_LeafNoderepr(self):
        node = LeafNode(tag="a", value="one", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.__repr__(), f"LeafNode({node.tag}, {node.value}, {node.props})")

    def test_to_html_no_tag(self):
        node = LeafNode(tag=None, value="Hello, World")
        self.assertEqual(node.to_html(), "Hello, World")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>")
    

if __name__ == "__main__":
    unittest.main()