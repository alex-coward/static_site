import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

class Test_markdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class Test_block_to_block_type(unittest.TestCase):
    def test_heading(self):
        block = "###### Hello World!"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    def test_code(self):
        block = "```\n" \
                "This is a code block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    def test_quote(self):
        block = "> This is a quote block\n" \
                ">That_includes several lines!"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    def test_unordered_list(self):
        block = "- This is an unordered list\n" \
                "- With 2 items!"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    def test_ordered_list(self):
        block = "1. Hello\n" \
                "2. World!"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

class Test_markdown_to_html_node(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )


if __name__ == "__main__":
    unittest.main()