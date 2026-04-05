from textnode import TextNode, TextType
from htmlnode import LeafNode
from block_markdown import markdown_to_html_node
import sys

import os
import shutil
import re

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

def main():
    copy_content("static", "docs")

def copy_content(src, dst):
    if not os.path.exists(src):
        raise Exception("Source path does not exist")
    if os.path.exists(dst):
        shutil.rmtree(dst)
        os.mkdir(dst)
    else:
        os.mkdir(dst)
    src_items = os.listdir(src)
    for src_item in src_items:
        item_path = os.path.join(src, src_item)
        print(item_path)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dst)
        else:
            sub_dst = os.path.join(dst, src_item)
            copy_content(item_path, sub_dst)

    generate_pages_recursive(dir_path_content="content", template_path="template.html",
                              dest_dir_path="docs", basepath=basepath)

def extract_title(markdown):
    h1 = re.search(r"#.*", markdown)
    if not h1:
        raise Exception("No h1 header")
    return h1.group().strip()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dir_path_content):
        raise Exception("Content path does not exist")
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    cont_items = os.listdir(dir_path_content)
    for cont_item in cont_items:
        item_path = os.path.join(dir_path_content, cont_item)
        if os.path.isfile(item_path):
            generate_page(item_path, template_path, dest_dir_path, basepath)

        else:
            sub_dst = os.path.join(dest_dir_path, cont_item)
            generate_pages_recursive(item_path, template_path, sub_dst, basepath)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        src_md = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(src_md)
    html = html_node.to_html()
    title = extract_title(src_md)
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace("href=", f"href={basepath}")
    template = template.replace("src=", f"src={basepath}")

    filename = os.path.basename(from_path)
    file_no_ext = os.path.splitext(filename)[0]
    html_file = file_no_ext + ".html"
    dest_file_path = os.path.join(dest_path, html_file)
    with open(dest_file_path, "w") as f:
        f.write(template)

main()