class HTMLNode:

    def __init__(self, tag: str = None, value: str = None, children: list[object] = None, props: dict[str] = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        # raise NotImplementedError
        children_str = ""

        for child in self.children:
            children_str += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>"

    def props_to_html(self) -> str | None:
        if self.props is None:
            return ""

        props_string = ""

        for prop, value in self.props.items():
            props_string += f" {prop}=\"{value}\""

        return props_string

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):

    def __init__(self, tag: str, children: list[object], props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required for object of type ParentNode")

        if not self.children:
            raise ValueError("children is required for object of type ParentNode")

        children_str = ""

        for child in self.children:
            children_str += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>"