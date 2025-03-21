import unittest

from blocks import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_init(self):
        htmlnode = HTMLNode("h1", "title")
        self.assertEqual("h1", htmlnode.tag)
        self.assertEqual("title", htmlnode.value)
        self.assertEqual(None, htmlnode.children)
        self.assertEqual(None, htmlnode.props)

    def test_children(self):
        htmlnodeChild = HTMLNode("span", "title")
        children = [htmlnodeChild]
        htmlnode = HTMLNode("h1", None, children)
        self.assertEqual("title", htmlnode.children[0].value)

    def test_props(self):
        props = {"href": "https://example.org"}
        htmlnode = HTMLNode("a", "Test", None, props)
        self.assertEqual(' href="https://example.org"', htmlnode.props_to_html())

    def test_text(self):
        text_node = TextNode("Hello", TextType.TEXT)
        expected_html_node = LeafNode(None, "Hello")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), expected_html_node.to_html()
        )

    def test_bold(self):
        text_node = TextNode("Hello", TextType.BOLD)
        expected_html_node = LeafNode("b", "Hello")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), expected_html_node.to_html()
        )

    def test_italic(self):
        text_node = TextNode("Hello", TextType.ITALIC)
        expected_html_node = LeafNode("i", "Hello")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), expected_html_node.to_html()
        )

    def test_code(self):
        text_node = TextNode("Hello", TextType.CODE)
        expected_html_node = LeafNode("code", "Hello")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), expected_html_node.to_html()
        )

    def test_link(self):
        text_node = TextNode("Hello", TextType.LINK, "https://example.com")
        expected_html_node = LeafNode("a", "Hello", {"href": "https://example.com"})
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), expected_html_node.to_html()
        )

    def test_image(self):
        text_node = TextNode("Hello", TextType.IMAGE, "https://example.com/image.jpg")
        expected_html_node = LeafNode(
            "img", "", {"src": "https://example.com/image.jpg", "alt": "Hello"}
        )
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), expected_html_node.to_html()
        )

    def test_invalid_text_type(self):
        text_node = TextNode("Hello", TextType.TEXT)
        text_node.text_type = "invalid"
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

    def test_link_without_url(self):
        text_node = TextNode("Hello", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node).to_html()

    def test_image_without_url(self):
        text_node = TextNode("Hello", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

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
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()  #
