from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props)
        self.tag = tag
        self.value = value
        self.props = props
        self.children = []

    def to_html(self):
        """Returns an HTML formatted string from the LeafNode. Usually <tag>value</tag>; special cases for images(tag='img') and link(tag='a') LeafNodes. Requires a value."""
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        if self.tag == "img":
            if self.props is None:
                raise ValueError("image props may not be None")
            return f'<{self.tag} src="{self.props.get("src")}.jpg" alt="{self.props.get("alt")}" />'
        if self.tag == "a":
            if self.props is None:
                raise ValueError("link props may not be None")
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
