import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_uneq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_uneq_url_none(self):
        none_url = TextNode("This is a text node", TextType.BOLD)
        has_url = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual(none_url, has_url)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, None)
        self.assertEqual(leaf_node.value, "This is a text node")
        self.assertEqual(leaf_node.to_html(), "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "This is a text node")
        self.assertEqual(leaf_node.to_html(), "<b>This is a text node</b>")

    def test_italic_text(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "i")
        self.assertEqual(leaf_node.value, "This is a text node")
        self.assertEqual(leaf_node.to_html(), "<i>This is a text node</i>")

    def test_code_text(self):
        node = TextNode("This is a text node", TextType.CODE)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "code")
        self.assertEqual(leaf_node.value, "This is a text node")
        self.assertEqual(leaf_node.to_html(), "<code>This is a text node</code>")

    def test_link_text(self):
        node = TextNode("This is a text node", TextType.LINKS, "https://www.google.com")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "a")
        self.assertEqual(leaf_node.value, "This is a text node")
        self.assertEqual(
            leaf_node.to_html(),
            '<a href="https://www.google.com">This is a text node</a>',
        )

    def test_image_text(self):
        node = TextNode(
            "This is a text node", TextType.IMAGES, "https://www.google.com"
        )
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "img")
        self.assertEqual(leaf_node.value, "")
        self.assertEqual(
            leaf_node.props,
            {"src": "https://www.google.com", "alt": "This is a text node"},
        )
        self.assertEqual(
            leaf_node.to_html(),
            '<img src="https://www.google.com.jpg" alt="This is a text node" />',
        )


if __name__ == "__main__":
    unittest.main()
