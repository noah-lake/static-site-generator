from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, children, props)
        self.tag = tag
        self.children = children
        self.props = props
        self.value = None

    def to_html(self):
        """Returns a string of HTML formatted text for every child LeafNode."""
        if self.tag is None:
            raise ValueError("tag cannot be None")
        if self.children is None:
            raise ValueError("children cannot be None")

        return_str = ""
        for child in self.children:
            if isinstance(child, ParentNode):
                return_str = return_str + child.to_html()
            elif isinstance(child, LeafNode):
                return_str = return_str + child.to_html()
        return f"<{self.tag}>{return_str}</{self.tag}>"
