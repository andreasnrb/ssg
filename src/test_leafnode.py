import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        htmlnode = LeafNode("h1", "title")
        self.assertEqual("<h1>title</h1>", htmlnode.to_html())

    def test_to_html_none(self):
        htmlnode = LeafNode(None, "title")
        self.assertEqual("title", htmlnode.to_html())

    def test_to_html2(self):
        htmlnode = LeafNode("span", "title")
        self.assertEqual("<span>title</span>", htmlnode.to_html())

    def test_props(self):
        props = {"href": "https://example.org"}
        htmlnode = LeafNode("a", "Test", props)
        self.assertEqual('<a href="https://example.org">Test</a>', htmlnode.to_html())

    def test_props2(self):
        props = {"href": "https://example.org", "class": "link"}
        htmlnode = LeafNode("a", "Test", props)
        self.assertEqual(
            '<a href="https://example.org" class="link">Test</a>', htmlnode.to_html()
        )

    def test_empty_tag_with_props(self):
        props = {"href": "https://example.org", "class": "link"}
        htmlnode = LeafNode(None, "Test", props)
        with self.assertRaises(ValueError):
            htmlnode.to_html()


if __name__ == "__main__":
    unittest.main()
