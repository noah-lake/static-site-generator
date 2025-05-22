import re
from parentnode import ParentNode
from textnode import TextType, TextNode, text_node_to_html_node
from enum import Enum


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Formats each TextNode object in a list (old_nodes) based on their delimeter and text type. Returns a list of TextNode objects with an altered self.text_type attribute where appropriate"""
    new_nodes = []
    for node in old_nodes:
        if (
            node.text_type != TextType.TEXT
        ):  # If a node isn't a basic text type, then we can assume that it has already been formatted...
            new_nodes.append(node)  # ...and subsequently chuck it into our return list
            continue
        delimiter_count = node.text.count(delimiter)
        if delimiter_count <= 1:
            new_nodes.append(
                node
            )  # If there is one or fewer delimiters, then the markdown is invalid and we can return it untouched.
        if (
            delimiter_count >= 2
        ):  # If we can find two of the delimiters, then we're in business.
            text = node.text
            if text.startswith(
                delimiter
            ):  # If our text starts with a delimiter, then we need to handle them differently
                text = text[len(delimiter) :]  # Remove the first delimiter
                split_text = text.split(
                    delimiter, maxsplit=1
                )  # Split until the end of that first delimiter
                split_node = [
                    TextNode(
                        split_text[0], text_type
                    ),  # The first element is the formatted text
                    TextNode(split_text[1], TextType.TEXT),  # The second is normal text
                ]
            # To avoid causing problems with order, we check if we have eactly one delimiter set left and if that delimiter set ends at the end.
            elif delimiter_count == 2 and text.endswith(delimiter):
                text = text[: -len(delimiter)]  # Cut off the final delimiter
                split_text = text.split(
                    delimiter
                )  # Split the text in half on the remaining delimiter
                split_node = [
                    TextNode(
                        split_text[0], TextType.TEXT
                    ),  # Assign everything before as text type
                    TextNode(
                        split_text[1], text_type
                    ),  # Assign everything after as the target type
                ]
            else:
                split_text = node.text.split(
                    delimiter, maxsplit=2
                )  # Split around our delimiters
                # Elements 1 and 3 are outside of the delimiters and should be returned as text type TextNodes
                split_node = [
                    TextNode(split_text[0], TextType.TEXT),
                    TextNode(
                        split_text[1], text_type
                    ),  # Element 2 is between the delimiters and should be reutrned as our target text type.
                    TextNode(split_text[2], TextType.TEXT),
                ]
            # Recur the function with our split_node as old_nodes, leaving other arguments unchanged.
            new_nodes.extend(split_nodes_delimiter(split_node, delimiter, text_type))
    return new_nodes


def extract_markdown_images(text):
    """Extracts anything that matches markdown image formatting '![{any text}]({any text})' is captured first as-is, then as a list of tuples containing the alt text and URL"""
    full_image_md = re.findall(
        r"(!\[[^\[\]]*\]\([^\(\)]*\))", text
    )  # returns a list of untouched md
    extracted = re.findall(
        r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text
    )  # returns a list of tuples
    return extracted, full_image_md


def extract_markdown_links(text):
    """Extracts anything that matches markdown link formatting '[{any text}]({any text})' is captured first as-is, then as a list of tuples containing the anchor text and URL"""
    full_link_md = re.findall(
        r"((?<!!)\[[^\[\]]*\]\([^\(\)]*\))", text
    )  # returns a list of untouched md
    extracted = re.findall(
        r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text
    )  # returns a list of tuples
    return extracted, full_link_md


def split_nodes_image(old_nodes):
    """Accepts a list of nodes and splits them into new nodes if they contain a markdown-formatted image or images"""
    new_nodes = []
    for node in old_nodes:
        # If the node isn't a text node, it has already been formatted and should not be touched
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # We extract any strings matching markdown image formatting, then count how many there are. If zero, then there is nothing to format and we put the node into the return list without further modification
        extracted_images = extract_markdown_images(node.text)
        image_count = len(extracted_images[1])
        if image_count == 0:
            new_nodes.append(node)

        elif image_count >= 1:
            text = node.text
            # extract_markdown_links() returns a tuple containing a list of tuples and a list of strings, in that order. The list of tuples [index 0] contains the extracted alt text and image src. We want to pull the raw markdown string from the list of strings [index 1]. Because of how we're recuring through a list of nodes, we only care about the first element of that list of strings.
            converted_tuples = extracted_images[0]
            current_image_md = extracted_images[1][0]

            # If the text starts or ends with the image, then we handle them slightly differently.
            # This differentiation is technically uneccessary, since it would just create a TextNode with an empty .text attribute, which we later clean out. We see this happen when the node contains nothing but an image
            if text.startswith(current_image_md):
                text = text[len(current_image_md) :]
                split_node = [
                    # converted_tuples (our list of tuples from extracted_images) contains the alt text first and the src second
                    TextNode(
                        converted_tuples[0][0],
                        TextType.IMAGES,
                        converted_tuples[0][1],
                    ),
                    TextNode(text, TextType.TEXT),
                ]

            elif image_count == 1 and text.endswith(current_image_md):
                text = text[: -len(current_image_md)]
                split_node = [
                    TextNode(text, TextType.TEXT),
                    TextNode(
                        converted_tuples[0][0],
                        TextType.IMAGES,
                        converted_tuples[0][1],
                    ),
                ]

            else:
                text = text.split(current_image_md, maxsplit=1)
                split_node = [
                    TextNode(text[0], TextType.TEXT),
                    TextNode(
                        converted_tuples[0][0],
                        TextType.IMAGES,
                        converted_tuples[0][1],
                    ),
                    TextNode(text[1], TextType.TEXT),
                ]

            # Recur the function to check if there are any more images that need converting
            new_nodes.extend(split_nodes_image(split_node))
    return new_nodes


# split_nodes_link functions almost identically to split_nodes-image.
def split_nodes_link(old_nodes):
    """Accepts a list of nodes and splits them into new nodes if they contain a markdown formatted link"""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_links = extract_markdown_links(node.text)
        link_count = len(extracted_links[1])
        if link_count == 0:
            new_nodes.append(node)

        elif link_count >= 1:
            text = node.text
            converted_tuples = extracted_links[0]
            current_link_md = extracted_links[1][0]

            if text.startswith(current_link_md):
                text = text[len(current_link_md) :]
                split_node = [
                    TextNode(
                        converted_tuples[0][0],
                        TextType.LINKS,
                        converted_tuples[0][1],
                    ),
                    TextNode(text, TextType.TEXT),
                ]

            elif link_count == 1 and text.endswith(current_link_md):
                text = text[: -len(current_link_md)]
                split_node = [
                    TextNode(text, TextType.TEXT),
                    TextNode(
                        converted_tuples[0][0],
                        TextType.LINKS,
                        converted_tuples[0][1],
                    ),
                ]

            else:
                text = text.split(current_link_md, maxsplit=1)
                split_node = [
                    TextNode(text[0], TextType.TEXT),
                    TextNode(
                        converted_tuples[0][0],
                        TextType.LINKS,
                        converted_tuples[0][1],
                    ),
                    TextNode(text[1], TextType.TEXT),
                ]

            new_nodes.extend(split_nodes_link(split_node))
    return new_nodes


def text_to_textnodes(text):
    """Calls split_nodes_delimiter for each of the inline text types, followed by split_nodes_image and split_nodes_link, then cleans out any TextNodes with an empty .text attribute"""
    node = TextNode(text, TextType.TEXT)
    bold_formatted = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic_formatted = split_nodes_delimiter(bold_formatted, "_", TextType.ITALIC)
    code_formatted = split_nodes_delimiter(italic_formatted, "`", TextType.CODE)
    image_formatted = split_nodes_image(code_formatted)
    link_formatted = split_nodes_link(image_formatted)
    return [node for node in link_formatted if len(node.text) > 0]


def markdown_to_blocks(markdown):
    """Splits a string of markdown formatted text (the whole document) into blocks of text. Cleans out any whitespace and trailing new lines, as well as any blocks with no text in them"""
    formatted_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        format = block.strip()
        formatted_blocks.append(format.strip("\n"))
    return [block for block in formatted_blocks if len(block) > 0]


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def block_to_block_type(block):
    """Assigns a BlockType to each block for easier handling later."""
    # If the block starts with six or fewer # symbols followed by a space, it is a heading
    if block.startswith("#"):
        num_hashtags = re.findall(r"(^\#+ )", block)
        if len(num_hashtags[0]) < 7:
            return BlockType.HEADING

    # If the block starts and ends with three graves, it is a code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # If each line in the block starts with a ">", it is a quote
    if block.startswith(">"):
        lines = block.splitlines()
        count = 0
        for line in lines:
            if line.startswith(">"):
                count += 1
        if count == len(lines):
            return BlockType.QUOTE

    # If each line of the block starts with a hyphen followed by a space, it is an unordered list
    if block.startswith("- "):
        lines = block.splitlines()
        count = 0
        for line in lines:
            if line.startswith("- "):
                count += 1
        if count == len(lines):
            return BlockType.UNORDERED_LIST

    # If each line of the block starts with a number followed by a period and a space, and if that number increases by one for each subsequent line in the block, then the block is an ordered list
    if block[0].isdigit():
        last_number = int(block[0]) - 1
        lines = block.splitlines()
        for line in lines:
            if int(line[0]) == last_number + 1 and line[1:3] == ". ":
                return BlockType.ORDERED_LIST

    # If the block isn't any of the other types, it is a paragraph
    return BlockType.PARAGRAPH


def text_to_children(block):
    """Breaks down the text of a block into a series of TextNodes, then converts them into LeafNodes and returns them as a list. Intended to be used to make ParentNodes"""
    children = []
    nodes = text_to_textnodes(block)
    for node in nodes:
        child = text_node_to_html_node(node)
        children.append(child)
    return children


def heading_block_to_html_node(block):
    """Counts the number of hashtags that the heading block starts with to create a tag, then strips the hashtags and converts the cleaned text into child LeafNodes, and finally creates a ParentNode for the heading block, using the created tag"""
    hashtags = re.findall(r"(^\#+ )", block)
    tag = f"h{len(hashtags[0]) - 1}"
    text = block.strip(hashtags[0])
    children = text_to_children(text)
    return ParentNode(tag=tag, children=children)


def code_block_to_html_node(block):
    """Strips the graves and newlines from the code block, then tags it and converts it directly into a LeafNode"""
    cleaned = block.strip("`")
    cut = cleaned.lstrip("\n")
    text = f"<pre><code>{cut}</code></pre>"
    node = TextNode(text, TextType.TEXT)
    return text_node_to_html_node(node)


def quote_block_to_html_node(block):
    """Strips the less than symbols from each line in the quote block, then converts the cleaned text into child LeafNodes, and finally creates a ParentNode for the quote block"""
    lines = block.splitlines()
    text = ""
    for line in lines:
        text += line.strip(">")
    children = text_to_children(text.strip())
    return ParentNode(tag="blockquote", children=children)


def unordered_list_to_html_node(block):
    """Strips the hyphen and space from each line in the unordred list, then tags each line as a list and converts the text into child LeafNodes, and finally creates a ParentNode for the unordered list."""
    lines = block.splitlines()
    text = ""
    for line in lines:
        text += f"<li>{line.strip('- ')}</li>"
    children = text_to_children(text)
    return ParentNode(tag="ul", children=children)


def ordered_list_to_html_node(block):
    """Removes the first three characters (usually a number followed by a dot and a space) from each line of the ordered list block, then tags each line as a list and converts the text into child LeafNodes, and finally creates a ParentNode for the ordered list"""
    lines = block.splitlines()
    text = ""
    for line in lines:
        text += f"<li>{line[3:]}</li>"
    children = text_to_children(text)
    return ParentNode(tag="ol", children=children)


def paragraph_block_to_html_node(block):
    """Replaces each instance of \n with a space, then converts the text into child LeafNodes and creates a ParentNode for the paragraph"""
    text = block.replace("\n", " ")
    children = text_to_children(text)
    return ParentNode(tag="p", children=children)


def markdown_to_html_node(markdown):
    """Loops through each block of a markdown formatted document and converts each block into an ParentNode, then creates a final ParentNode for the document tagged as 'div'"""
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            children.append(heading_block_to_html_node(block))
        if block_type == BlockType.CODE:
            children.append(code_block_to_html_node(block))
        if block_type == BlockType.QUOTE:
            children.append(quote_block_to_html_node(block))
        if block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html_node(block))
        if block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_block_to_html_node(block))
    return ParentNode(tag="div", children=children)


def extract_title(markdown):
    """Ensures that the document starts with a tilte header and extracts its text"""
    if not markdown.startswith("# "):
        raise Exception("Document must start with an h1 header")
    lines = markdown.splitlines()
    return lines[0].strip("# ")
