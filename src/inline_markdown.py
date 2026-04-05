from textnode import TextNode, TextType
from htmlnode import LeafNode
import re

def text_node_to_html_node(text_node: TextNode):
    text = text_node.text
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text)

    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text)

    if text_node.text_type ==  TextType.ITALIC:
        return LeafNode(tag="i", value=text)

    if text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text)
    if text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text, props={"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text})
    raise ValueError(f"invalid text type: {text_node.text_type}")

def text_to_textnodes(text):
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes = split_nodes_delimiter(old_nodes=nodes, delimiter="**", text_type=TextType.BOLD)
    nodes = split_nodes_delimiter(old_nodes=nodes, delimiter="_", text_type=TextType.ITALIC)
    nodes = split_nodes_delimiter(old_nodes=nodes, delimiter="`", text_type=TextType.CODE)
    nodes = split_nodes_image(old_nodes=nodes)
    nodes = split_nodes_link(old_nodes=nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text_list = node.text.split(delimiter)
        if (len(node_text_list) % 2 == 0):
            raise Exception(f"Not valid markdown for {text_type}")
        for i in range(len(node_text_list)):
            if node_text_list[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text=node_text_list[i], text_type=TextType.TEXT))
            else:
                new_nodes.append(TextNode(text=node_text_list[i], text_type=text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(text=sections[0], text_type=TextType.TEXT))
            new_nodes.append(TextNode(text=image[0], text_type=TextType.IMAGE, url=image[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text=text, text_type=TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(text=sections[0], text_type=TextType.TEXT))
            new_nodes.append(TextNode(text=link[0], text_type=TextType.LINK, url=link[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text=text, text_type=TextType.TEXT))
    return new_nodes

def extract_markdown_images(text: str):
    images = re.findall(r"!\[(.+?)\]\((.+?)\)", text)
    return images

def extract_markdown_links(text: str):
    links = re.findall(r"\[(.+?)\]\((.+?)\)", text)
    return links