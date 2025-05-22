import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        node = LeafNode(
            tag="a", value="Click me!", props={"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_b(self):
        node = LeafNode(tag="b", value="Bold text!")
        self.assertEqual(node.to_html(), "<b>Bold text!</b>")

    def test_leaf_to_html_img(self):
        node = LeafNode(
            tag="img",
            value="",
            props={"src": "https://www.google.com", "alt": "Alt text"},
        )
        self.assertEqual(
            node.to_html(), '<img src="https://www.google.com.jpg" alt="Alt text" />'
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(value="Normal text!")
        self.assertEqual(node.to_html(), "Normal text!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode(tag="b")
        with self.assertRaises(ValueError, msg="value may not be None"):
            node.to_html()

    def test_leaf_to_html_img_no_prop(self):
        node = LeafNode(tag="img", value="Dummy text")
        with self.assertRaises(ValueError, msg="image props may not be None"):
            node.to_html()

    def test_leaf_to_html_link_no_prop(self):
        node = LeafNode(tag="a", value="Click me!")
        with self.assertRaises(ValueError, msg="link props cannot be None"):
            node.to_html()
