import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_four_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_no_children(self):
        node = ParentNode("p")
        with self.assertRaises(ValueError, msg="children cannot be None"):
            node.to_html()

    def test_to_html_with_no_tag(self):
        node = ParentNode(
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        with self.assertRaises(ValueError, msg="tag cannot be None"):
            node.to_html()

    def test_to_html_parent_and_leaf_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode("div", [LeafNode("i", "italic text")]),
            ],
        )
        self.assertEqual(
            node.to_html(), "<p><b>Bold text</b><div><i>italic text</i></div></p>"
        )

    def test_to_html_with_child_with_no_tag(self):
        node = ParentNode("p", [ParentNode(children=[LeafNode("b", "Bold text")])])
        with self.assertRaises(ValueError, msg="tag cannot be None"):
            node.to_html()
