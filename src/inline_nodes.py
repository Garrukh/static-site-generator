from textnode import TextNode, TextType
from regex import extract_markdown_images, extract_markdown_links

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Matching ending delimeter not found!")

        for i, new_node_text in enumerate(node.text.split(delimiter)):
            if new_node_text == "":
                continue
            if i % 2:
                new_nodes.append(TextNode(new_node_text, text_type))
            else:
                new_nodes.append(TextNode(new_node_text, TextType.TEXT))

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_images = extract_markdown_images(node.text)
        if not extracted_images:
            new_nodes.append(node)
            continue

        remaining_node_text = node.text
        for image_text, image_location in extracted_images:
            sections = remaining_node_text.split(f"![{image_text}]({image_location})", 1)
            
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_text, TextType.IMAGE, image_location))
            
            remaining_node_text = sections[1]

        if remaining_node_text:
            new_nodes.append(TextNode(remaining_node_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_links = extract_markdown_links(node.text)
        if not extracted_links:
            new_nodes.append(node)
            continue

        remaining_node_text = node.text

        for link_text, link_location in extracted_links:
            sections = remaining_node_text.split(f"[{link_text}]({link_location})", 1)
            
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_location))
            
            remaining_node_text = sections[1]

        if remaining_node_text:
            new_nodes.append(TextNode(remaining_node_text, TextType.TEXT))

    return new_nodes