from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props)
        self.tag = tag
        self.value = value
        self.props = props
        self.children = []

    def to_html(self):
        """Returns an HTML formatted string from the LeafNode. Usually <tag>value</tag>; special cases for images(tag='img') and link(tag='a') LeafNodes. Requires a value and does not accept children."""
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        if self.tag == "img":
            if self.props is None:
                raise ValueError("image props may not be None")
            url = self.props.get("src")
            alt = self.props.get("alt")
            return f'<{self.tag} src="{url}" alt="{alt}" />'
        if self.tag == "a":
            if self.props is None:
                raise ValueError("link props may not be None")
            html_props = self.props_to_html()
            return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"
        # If it's not an image or a link, it can be tagged normally.
        return f"<{self.tag}>{self.value}</{self.tag}>"
