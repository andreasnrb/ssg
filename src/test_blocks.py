import unittest

from blocks import (BlockType, block_to_block_type, code_to_html_node,
                    heading_to_html_node, olist_to_html_node,
                    paragraph_to_html_node, quote_to_html_node,
                    ulist_to_html_node)
from htmlnode import ParentNode


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_multi_level_heading(self):
        block = "### Multi-level heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> Quote\n> Another line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_single_line_code_block(self):
        block = "```single line code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_multi_line_quote_block(self):
        block = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_invalid_ordered_list(self):
        block = "1. Item 1\n3. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_unordered_list(self):
        block = "- Item 1\nItem 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_quote_block(self):
        block = "> Quote\nNot a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_code_block(self):
        block = "```code"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_long_paragraph(self):
        block = "This is a very long paragraph that spans multiple lines.\nIt has multiple sentences and is quite verbose."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_with_invalid_item(self):
        block = """1. Item 1
        2. Item 2
        This is not a list item
        3. Item 3"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_with_invalid_item(self):
        block = """- Item 1
        - Item 2
        This is not a list item
        - Item 3"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_single_line_paragraph(self):
        block = "This is a single line paragraph."
        expected_html_node = ParentNode("p", ["This is a single line paragraph."])
        self.assertEqual(paragraph_to_html_node(block).tag, expected_html_node.tag)
        self.assertEqual(
            len(paragraph_to_html_node(block).children),
            len(expected_html_node.children),
        )

    def test_multi_line_paragraph(self):
        block = "This is a multi-line\nparagraph with two lines."
        expected_html_node = ParentNode(
            "p", ["This is a multi-line paragraph with two lines."]
        )
        self.assertEqual(paragraph_to_html_node(block).tag, expected_html_node.tag)
        self.assertEqual(
            len(paragraph_to_html_node(block).children),
            len(expected_html_node.children),
        )

    def test_empty_paragraph(self):
        block = ""
        expected_html_node = ParentNode("", [])
        self.assertEqual(paragraph_to_html_node(block).tag, expected_html_node.tag)
        self.assertEqual(
            len(paragraph_to_html_node(block).children),
            len(expected_html_node.children),
        )

    def test_paragraph_with_multiple_spaces(self):
        block = "This   is   a   paragraph   with   multiple   spaces."
        expected_html_node = ParentNode(
            "p", ["This is a paragraph with multiple spaces."]
        )
        self.assertEqual(paragraph_to_html_node(block).tag, expected_html_node.tag)
        self.assertEqual(
            len(paragraph_to_html_node(block).children),
            len(expected_html_node.children),
        )

    def test_paragraph_with_newlines_at_end(self):
        block = "This is a paragraph.\n\n"
        expected_html_node = ParentNode("p", ["This is a paragraph."])
        self.assertEqual(paragraph_to_html_node(block).tag, expected_html_node.tag)
        self.assertEqual(
            len(paragraph_to_html_node(block).children),
            len(expected_html_node.children),
        )

    def test_heading_level_1(self):
        block = "# Heading Level 1"
        expected_html_node = ParentNode("h1", ["Heading Level 1"])
        self.assertEqual(heading_to_html_node(block).tag, expected_html_node.tag)
        self.assertEqual(
            len(heading_to_html_node(block).children), len(expected_html_node.children)
        )

    def test_heading_level_2(self):
        block = "## Heading Level 2"
        expected_html_node = ParentNode("h2", ["Heading Level 2"])
        self.assertEqual(heading_to_html_node(block).tag, expected_html_node.tag)
        self.assertEqual(
            len(heading_to_html_node(block).children), len(expected_html_node.children)
        )

    def test_heading_level_3(self):
        block = "### Heading Level 3"
        expected_html_node = ParentNode("h3", ["Heading Level 3"])
        self.assertEqual(heading_to_html_node(block).tag, expected_html_node.tag)
        self.assertEqual(
            len(heading_to_html_node(block).children), len(expected_html_node.children)
        )

    def test_heading_level_6(self):
        block = "###### Heading Level 6"
        expected_html_node = ParentNode("h6", ["Heading Level 6"])
        self.assertEqual(heading_to_html_node(block).tag, expected_html_node.tag)
        self.assertEqual(
            len(heading_to_html_node(block).children), len(expected_html_node.children)
        )

    def test_heading_with_spaces(self):
        block = "#   Heading Level 1"
        expected_html_node = ParentNode("h1", ["Heading Level 1"])
        self.assertEqual(heading_to_html_node(block).tag, expected_html_node.tag)
        self.assertEqual(
            len(heading_to_html_node(block).children), len(expected_html_node.children)
        )

    def test_heading_with_trailing_spaces(self):
        block = "# Heading Level 1   "
        expected_html_node = ParentNode("h1", ["Heading Level 1"])
        self.assertEqual(heading_to_html_node(block).tag, expected_html_node.tag)
        self.assertEqual(
            len(heading_to_html_node(block).children), len(expected_html_node.children)
        )

    def test_empty_heading(self):
        block = "#"
        with self.assertRaises(ValueError):
            heading_to_html_node(block)

    def test_invalid_heading(self):
        block = "#### Heading Level 4 #"
        with self.assertRaises(ValueError):
            heading_to_html_node(block)

    def test_valid_code_block(self):
        block = """
```
This is a code block
```
"""
        result = code_to_html_node(block)
        self.assertEqual(result.tag, "pre")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "code")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(result.children[0].children[0].value, "This is a code block")

    def test_code_block_with_multiple_lines(self):
        block = """
```
This is a code block
with multiple lines
```
"""
        result = code_to_html_node(block)
        self.assertEqual(result.tag, "pre")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "code")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(
            result.children[0].children[0].value,
            "This is a code block\nwith multiple lines",
        )

    """
    def test_code_block_with_trailing_spaces(self):
        block = "```This is a code block   ```"
        result = code_to_html_node(block)
        self.assertEqual(result.tag, "pre")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "code")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(
            result.children[0].children[0].value, "This is a code block   "
        )
    """

    def test_code_block_without_trailing_backticks(self):
        block = "```This is a code block"
        with self.assertRaises(ValueError):
            code_to_html_node(block)

    def test_code_block_without_leading_backticks(self):
        block = "This is a code block```"
        with self.assertRaises(ValueError):
            code_to_html_node(block)

    def test_empty_code_block(self):
        block = "``````"
        result = code_to_html_node(block)
        self.assertEqual(result.tag, "pre")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "code")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(result.children[0].children[0].value, "")

    def test_valid_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        result = olist_to_html_node(block)
        self.assertEqual(result.tag, "ol")
        self.assertEqual(len(result.children), 3)
        for i, child in enumerate(result.children):
            self.assertEqual(child.tag, "li")
            self.assertEqual(len(child.children), 1)
            self.assertEqual(child.children[0].value, f"Item {i+1}")

    """
    def test_ordered_list_with_multiple_lines(self):
        block = "1. Item 1 with multiple lines\n    that are wrapped\n2. Item 2"
        result = olist_to_html_node(block)
        self.assertEqual(result.tag, "ol")
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.children[0].tag, "li")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(
            result.children[0].children[0].value,
            "Item 1 with multiple lines    that are wrapped",
        )
        self.assertEqual(result.children[1].tag, "li")
        self.assertEqual(len(result.children[1].children), 1)
        self.assertEqual(result.children[1].children[0].value, "Item 2")
    """

    def test_ordered_list_with_trailing_spaces(self):
        block = "1. Item 1   \n2. Item 2   "
        result = olist_to_html_node(block)
        self.assertEqual(result.tag, "ol")
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.children[0].tag, "li")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(result.children[0].children[0].value, "Item 1   ")
        self.assertEqual(result.children[1].tag, "li")
        self.assertEqual(len(result.children[1].children), 1)
        self.assertEqual(result.children[1].children[0].value, "Item 2   ")

    def test_valid_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        result = ulist_to_html_node(block)
        self.assertEqual(result.tag, "ul")
        self.assertEqual(len(result.children), 3)
        for i, child in enumerate(result.children):
            self.assertEqual(child.tag, "li")
            self.assertEqual(len(child.children), 1)
            self.assertEqual(child.children[0].value, f"Item {i+1}")

    """
    def test_unordered_list_with_multiple_lines(self):
        block = "- Item 1 with multiple lines\n    that are wrapped\n- Item 2"
        result = ulist_to_html_node(block)
        self.assertEqual(result.tag, "ul")
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.children[0].tag, "li")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(result.children[0].children[0].value, "Item 1 with multiple lines    that are wrapped")
        self.assertEqual(result.children[1].tag, "li")
        self.assertEqual(len(result.children[1].children), 1)
        self.assertEqual(result.children[1].children[0].value, "Item 2")
    """

    def test_unordered_list_with_trailing_spaces(self):
        block = "- Item 1   \n- Item 2   "
        result = ulist_to_html_node(block)
        self.assertEqual(result.tag, "ul")
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.children[0].tag, "li")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(result.children[0].children[0].value, "Item 1   ")
        self.assertEqual(result.children[1].tag, "li")
        self.assertEqual(len(result.children[1].children), 1)
        self.assertEqual(result.children[1].children[0].value, "Item 2   ")

    def test_valid_quote(self):
        block = "> This is a quote\n> with multiple lines"
        result = quote_to_html_node(block)
        self.assertEqual(result.tag, "blockquote")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(
            result.children[0].value, "This is a quote with multiple lines"
        )

    def test_quote_with_trailing_spaces(self):
        block = "> This is a quote   \n> with multiple lines   "
        result = quote_to_html_node(block)
        self.assertEqual(result.tag, "blockquote")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(
            result.children[0].value, "This is a quote with multiple lines"
        )

    def test_invalid_quote(self):
        block = "This is not a quote"
        with self.assertRaises(ValueError):
            quote_to_html_node(block)

    def test_quote_with_missing_leading_angle_bracket(self):
        block = "> This is a quote\nThis is not a quote"
        with self.assertRaises(ValueError):
            quote_to_html_node(block)


if __name__ == "__main__":
    unittest.main()
