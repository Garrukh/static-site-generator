from md_blocks import markdown_to_blocks, block_to_block_type, BlockType
from inline_nodes import text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node

def prepare_inline_child_nodes(text):
    text_nodes = text_to_textnodes(text)
    inline_children = []

    for child in text_nodes:
        inline_children.append(text_node_to_html_node(child))

    return inline_children

def handle_paragraph_block(block: str, tag: str) -> HTMLNode:
    children = prepare_inline_child_nodes(block.replace("\n", " "))

    return HTMLNode(tag, children=children)

def handle_quote_block(block: str, tag: str) -> HTMLNode:
    text = "\n".join([line.removeprefix("> ") for line in block.splitlines()])

    children = prepare_inline_child_nodes(text)

    return HTMLNode(tag, children=children)

def handle_code_block(block: str, tag: str) -> HTMLNode:
    text = block.strip("`").strip()
    child = LeafNode(tag, text)

    return HTMLNode("pre", children=[child])

def handle_unordered_list_block(block: str, tag: str) -> HTMLNode:
    children = []

    for line in block.splitlines():
        inline_nodes = prepare_inline_child_nodes(line.removeprefix("- "))

        children.append(HTMLNode("li", children=inline_nodes))

    return HTMLNode("ul", children=children)

def handle_ordered_list_block(block: str, tag: str) -> HTMLNode:
    children = []

    for line in block.splitlines():
        inline_nodes = prepare_inline_child_nodes(line[3:])

        children.append(HTMLNode("li", children=inline_nodes))

    return HTMLNode("ol", children=children)

def handle_heading_block(block: str, tag: str) -> HTMLNode:
    text = block.lstrip("# ")
    heading_level = len(block) - len(text) - 1
    children = prepare_inline_child_nodes(text)

    return HTMLNode(f"h{heading_level}", children=children)

def markdown_to_html_node(markdown) -> ParentNode:
    children = []

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        b_type = block_to_block_type(block)

        if b_type == BlockType.PARAGRAPH:
            children.append(handle_paragraph_block(block, b_type.value))

        if b_type == BlockType.QUOTE:
            children.append(handle_quote_block(block, b_type.value))

        if b_type == BlockType.CODE:
            children.append(handle_code_block(block, b_type.value))

        if b_type == BlockType.UNORDERED_LIST:
            children.append(handle_unordered_list_block(block, b_type.value))

        if b_type == BlockType.ORDERED_LIST:
            children.append(handle_ordered_list_block(block, b_type.value))

        if b_type == BlockType.HEADING:
            children.append(handle_heading_block(block, b_type.value))

    return ParentNode("div", children)