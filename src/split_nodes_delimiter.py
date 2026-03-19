from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            node_text_list = node.text.split(delimiter)
            if (len(node_text_list) % 2 == 0):
                raise Exception(f"Not valid markdown for {text_type}")
            else:
                for i in range(len(node_text_list)):
                    if i % 2 == 0:
                        new_nodes.append(TextNode(text=node_text_list[i], text_type=TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(text=node_text_list[i], text_type=text_type))

    return new_nodes

