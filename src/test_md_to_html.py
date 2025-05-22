import unittest
from md_to_html import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
)
from textnode import TextNode, TextType


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_split_node_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_multiple_delimiter_sets(self):
        node = TextNode(
            "This is `text` with `multiple code block` words", TextType.TEXT
        )
        first_run = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            first_run,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.CODE),
                TextNode(" with ", TextType.TEXT),
                TextNode("multiple code block", TextType.CODE),
                TextNode(" words", TextType.TEXT),
            ],
        )

    def test_different_delimiters(self):
        node = TextNode(
            "This is a text node with _italic_ and **bold** words", TextType.TEXT
        )
        first_run = split_nodes_delimiter([node], "_", TextType.ITALIC)
        second_run = split_nodes_delimiter(first_run, "**", TextType.BOLD)
        self.assertEqual(
            first_run,
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and **bold** words", TextType.TEXT),
            ],
        )
        self.assertEqual(
            second_run,
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" words", TextType.TEXT),
            ],
        )

    def test_non_text_type_nodes(self):
        node = TextNode("**This is a bold text node**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_many_delimiter_sets(self):
        node = TextNode(
            "`This` is `text` with `a` whole `bunch` of `code` text", TextType.TEXT
        )
        run = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            run,
            [
                TextNode("This", TextType.CODE),
                TextNode(" is ", TextType.TEXT),
                TextNode("text", TextType.CODE),
                TextNode(" with ", TextType.TEXT),
                TextNode("a", TextType.CODE),
                TextNode(" whole ", TextType.TEXT),
                TextNode("bunch", TextType.CODE),
                TextNode(" of ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_ends_with_delimiter(self):
        node = TextNode("This text ends with a `delimiter`", TextType.TEXT)
        run = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            run,
            [
                TextNode("This text ends with a ", TextType.TEXT),
                TextNode("delimiter", TextType.CODE),
            ],
        )

    def test_ends_with_double_delimiter(self):
        node = TextNode("This text ends with a **double delimiter**", TextType.TEXT)
        run = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            run,
            [
                TextNode("This text ends with a ", TextType.TEXT),
                TextNode("double delimiter", TextType.BOLD),
            ],
        )

    def test_tons_of_nodes(self):
        node1 = TextNode("This text has _italics_", TextType.TEXT)
        node2 = TextNode("This text has **bold**", TextType.TEXT)
        node3 = TextNode("This text has `code`", TextType.TEXT)
        first_run = split_nodes_delimiter([node1, node2, node3], "_", TextType.ITALIC)
        second_run = split_nodes_delimiter(first_run, "**", TextType.BOLD)
        third_run = split_nodes_delimiter(second_run, "`", TextType.CODE)
        self.assertEqual(
            first_run,
            [
                TextNode("This text has ", TextType.TEXT),
                TextNode("italics", TextType.ITALIC),
                TextNode("This text has **bold**", TextType.TEXT),
                TextNode("This text has `code`", TextType.TEXT),
            ],
        )
        self.assertEqual(
            second_run,
            [
                TextNode("This text has ", TextType.TEXT),
                TextNode("italics", TextType.ITALIC),
                TextNode("This text has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("This text has `code`", TextType.TEXT),
            ],
        )
        self.assertEqual(
            third_run,
            [
                TextNode("This text has ", TextType.TEXT),
                TextNode("italics", TextType.ITALIC),
                TextNode("This text has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("This text has ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_two_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            (
                [
                    ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                    ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
                ],
                [
                    "![rick roll](https://i.imgur.com/aKaOqIh.gif)",
                    "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                ],
            ),
        )

    def test_isolated_url(self):
        text = "This is text with an isolated (https://google.com/mess.gif) and a ![rick roll](https://i.imgur.com/aKa0qIh.gif)"
        self.assertEqual(
            extract_markdown_images(text),
            (
                [("rick roll", "https://i.imgur.com/aKa0qIh.gif")],
                ["![rick roll](https://i.imgur.com/aKa0qIh.gif)"],
            ),
        )

    def test_isolated_alt_text(self):
        text = "This is text with an isolated ![alt text] and a ![full link](https://i.imgur.com/mess.gif)"
        self.assertEqual(
            extract_markdown_images(text),
            (
                [("full link", "https://i.imgur.com/mess.gif")],
                ["![full link](https://i.imgur.com/mess.gif)"],
            ),
        )

    def test_no_links(self):
        text = "This text has no links"
        self.assertEqual(extract_markdown_images(text), ([], []))

    def test_www_link(self):
        text = "This is text with ![rick roll](https://www.google.com/mess.gif)"
        self.assertEqual(
            extract_markdown_images(text),
            (
                [("rick roll", "https://www.google.com/mess.gif")],
                ["![rick roll](https://www.google.com/mess.gif)"],
            ),
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_two_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            (
                [
                    ("to boot dev", "https://www.boot.dev"),
                    ("to youtube", "https://www.youtube.com/@bootdotdev"),
                ],
                [
                    "[to boot dev](https://www.boot.dev)",
                    "[to youtube](https://www.youtube.com/@bootdotdev)",
                ],
            ),
        )

    def test_no_links(self):
        text = "This is text with no links"
        self.assertEqual(extract_markdown_links(text), ([], []))

    def test_isolated_anchor_text(self):
        text = "This is text with [isolated anchor text] and a link [to boot dev](https://www.boot.dev)"
        self.assertEqual(
            extract_markdown_links(text),
            (
                [("to boot dev", "https://www.boot.dev")],
                ["[to boot dev](https://www.boot.dev)"],
            ),
        )

    def test_isolated_link(self):
        text = "This is text with (https://www.isolated.link) and a link [to youtube](https://www.youtube.com)"
        self.assertEqual(
            extract_markdown_links(text),
            (
                [("to youtube", "https://www.youtube.com")],
                ["[to youtube](https://www.youtube.com)"],
            ),
        )


class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_image_up_front(self):
        node = TextNode("![image](image.url) so I heard you like images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGES, "image.url"),
                TextNode(" so I heard you like images", TextType.TEXT),
            ],
        )


class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINKS, "https://www.youtube.com"),
            ],
        )

    def test_link_up_front(self):
        node = TextNode("[anchor text](link.url) I heard you like links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("anchor text", TextType.LINKS, "link.url"),
                TextNode(" I heard you like links", TextType.TEXT),
            ],
        )


class TestTextToTextnodes(unittest.TestCase):
    def test_several_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ],
        )

    def test_missing_bold(self):
        text = "This is text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ],
        )

    def test_missing_italic(self):
        text = "This is **text** with an italic word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an italic word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ],
        )

    def test_missing_code(self):
        text = "This is **text** with an _italic_ word and a code block and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a code block and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ],
        )

    def test_missing_image(self):
        text = "This is **text** with an _italic_ word and a `code block` and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(
                    " and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a ",
                    TextType.TEXT,
                ),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ],
        )

    def test_missing_link(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a link https://boot.dev"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a link https://boot.dev", TextType.TEXT),
            ],
        )

    def test_lots_of_bold(self):
        text = "This is **text** with an **italic** word and a **code block** and an **obi wan image** and a **link**"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.BOLD),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.BOLD),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.BOLD),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.BOLD),
            ],
        )

    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
