import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "example.org")
        node2 = TextNode("This is a text node", TextType.BOLD, "example.org")
        self.assertEqual(node, node2)

    def test_eq_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_eq_wrong_enum(self):
        node = TextNode("This is a text node", "test", None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertNotEqual(node, node2)

    def test_eq_empty_enum(self):
        node = TextNode("This is a text node", None, None)
        node2 = TextNode("This is a text node", None, None)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
