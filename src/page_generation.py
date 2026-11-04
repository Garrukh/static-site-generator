import os
import shutil

from regex import extract_title
from md_to_html import markdown_to_html_node

def generate_page(from_path: str, template_path:str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as md_file:
        md = md_file.read()
    with open(template_path) as template_file:
        template = template_file.read()

    title = extract_title(md)
    html_node = markdown_to_html_node(md)

    html = template.replace('{{ Title }}', title)
    html = html.replace('{{ Content }}', html_node.to_html())
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')

    with open(dest_path, mode="w") as dest_file:
        dest_file.write(html)

def generate_pages_recursive(from_path: str, template_path: str, to_path: str, basepath: str) -> None:
    if not os.path.exists(to_path):
        os.mkdir(to_path)

    for item in os.listdir(from_path):
        from_item_path = os.path.join(from_path, item)
        to_item_path = os.path.join(to_path, item).replace(".md", ".html")

        print(f" * {from_item_path} -> {to_item_path}")

        if os.path.isfile(from_item_path):
            generate_page(from_item_path, template_path, to_item_path, basepath)
        else:
            generate_pages_recursive(from_item_path, template_path, to_item_path, basepath)