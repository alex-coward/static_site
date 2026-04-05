from enum import Enum
import re
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED LIST"
    ORDERED_LIST = "ORDERED LIST"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            size = len(re.findall("#", block))
            tag = f"h{size}"
            text = block.replace("#", "").strip()
            children = text_to_children(text)
            heading = ParentNode(tag=tag, children=children)
            nodes.append(heading)
        elif block_type == BlockType.CODE:
            code = block.split("```\n")[1].replace("```", "")
            code_node = LeafNode(tag="code", value=code)
            code_parent = ParentNode(tag="pre", children=[code_node])
            nodes.append(code_parent)
        elif block_type == BlockType.QUOTE:
            block_text = block.replace("> ", "").replace(">", "")
            block_quote = LeafNode(tag="blockquote", value=block_text)
            nodes.append(block_quote)
        elif block_type == BlockType.UNORDERED_LIST:
            list_nodes = []
            list_items = re.findall(r"- (?:[^\n]+)?", block)
            for list_item in list_items:
                li_text = list_item.replace("- ", "")
                children = text_to_children(li_text)
                li_node = ParentNode(tag="li", children=children)
                list_nodes.append(li_node)
            unordered_list = ParentNode(tag="ul", children=list_nodes)
            nodes.append(unordered_list)
        elif block_type == BlockType.ORDERED_LIST:
            list_nodes = []
            list_items = block.split("\n")
            for list_item in list_items:
                li_text = list_item.split(". ")[1]
                children = text_to_children(li_text)
                li_node = ParentNode(tag="li", children=children)
                list_nodes.append(li_node)
            ordered_list = ParentNode(tag="ol", children=list_nodes)
            nodes.append(ordered_list)
        else:
            text = block.replace("\n", " ")
            children = text_to_children(text)
            paragraph = ParentNode(tag="p", children=children)
            nodes.append(paragraph)
    parent_node = ParentNode(tag="div", children=nodes)
    return parent_node



def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            clean_blocks.append(block)
    return clean_blocks


def block_to_block_type(block):
    if re.match(r"\A#{1,6} [^\n]*\Z", block):
        return BlockType.HEADING
    elif re.match(r"(?s)\A```\n.+```\Z", block):
        return BlockType.CODE
    elif re.match(r"\A(?:>(?:[^\n]+)?(?:\n|$))+\Z", block):
        return BlockType.QUOTE
    elif re.match(r"\A(?:- (?:[^\n]+)?(?:\n|$))+\Z", block):
        return BlockType.UNORDERED_LIST
    else:
        pattern = r"\A"
        newlines = re.findall("\n", block)
        for i in range(len(newlines)+1):
            pattern += fr"{i+1}. (?:[^\n]+)?(?:\n|$)\n?"
        pattern += r"\Z"
        if re.match(pattern, block):
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
