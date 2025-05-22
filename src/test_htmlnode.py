import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag=None,
            value=None,
            children=None,
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_uneq(self):
        node = HTMLNode(
            tag=None,
            value=None,
            children=None,
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        unexpected = "incorrect string"
        self.assertNotEqual(node.props_to_html(), unexpected)

    def test_props_to_html_populated(self):
        node = HTMLNode(
            tag="a tag",
            value="a value",
            children="a child",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_singlekv(self):
        node = HTMLNode(
            tag="a", value="Click me!", props={"href": "https://www.google.com"}
        )
        expected = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected)
