from textnode import TextNode, TextType
from htmlnode import LeafNode

def main():
    node = TextNode("Hello world", text_type=TextType("TEXT"), url="www.testing123.com")
    print(node)

def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == "TEXT":
        return LeafNode(tag=None, value=text_node.text)
    
    elif text_node.text_type == "BOLD":
        return LeafNode(tag="b", value=text_node.text)
    
    elif text_node.text_type == "ITALIC":
        return LeafNode(tag="i", value=text_node.text)
    
    elif text_node.text_type == "CODE":
        return LeafNode(tag="code", value=text_node.text)
    
    elif text_node.text_type == "LINK":
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    else:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    

main()