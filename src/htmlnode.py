class HTMLNode:
    
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None , props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        html = ""
        if self.props is not None:
            for key, value in self.props.items():
                html += f" {key}={value}"
        return html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
    def __eq__(self, other):
        if (self.tag == other.tag) and (self.value == other.value) and (self.children == other.children) and (self.props == other.props):
            return True
        return False

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str , props: dict | None = None):
        super().__init__(tag=tag, value=value, props=props)


    def to_html(self):
        if self.value is None:
            raise ValueError("All LeafNodes must have a value")
        if self.tag is None:
            return self.value
        prop_text = self.props_to_html()
        return f"<{self.tag}{prop_text}>{self.value}</{self.tag}>"
                
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict | None = None):
        super().__init__(tag=tag, value=None, children=children, props=props)


    def to_html(self):
        if self.tag is None:
            raise ValueError("All ParentNodes must have a tag")
        if self.children is None:
            raise ValueError("All ParentNodes must have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
            
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"