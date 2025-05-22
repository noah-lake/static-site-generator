class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # HTML tag name ("p", "a", "h1", etc.)
        self.value = value  # The actual text
        self.children = children  # A list of nodes that are children of this node
        self.props = props  # A dictionary of key-value pairs representing the attributes of the HTML tag

    def to_html(self):
        """Not implemented. To be overwritten by child classes."""
        raise NotImplementedError

    def props_to_html(self):
        """Returns element 1 = ' "element 2"' for each item in the properties list. Each string intentionally starts with a space."""
        if self.props is not None:
            return "".join(map(lambda x: f' {x[0]}="{x[1]}"', self.props.items()))
        return ""

    def __repr__(self):
        """Returns a string representation of the objects attributes."""
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props}"
