import re

def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def is_heading_block(block: str) -> bool:
    if re.fullmatch(r"^#{1,6} {1}.*$", block):
        return True
    return False

def is_code_block(block: str) -> bool:
    if re.fullmatch(r"^`{3}\n[\s\S]*`{3}$", block):
        return True
    return False

def is_quote_block(block: str) -> bool:
    if re.fullmatch(r"(?:^> ?.*\n?)+", block, flags=re.M):
        return True
    return False

def is_unordered_block(block: str) -> bool:
    if re.fullmatch(r"(?:^- {1}.*\n?)+", block, flags=re.M):
        return True
    return False

def is_ordered_list_block(block: str) -> bool:
    if not re.fullmatch(r"(?:^\d+\. {1}.*\n?)+", block, flags=re.M):
        return False
    
    leadin_numbers = [int(n) for n in re.findall(r"^\d+", block, flags=re.M)]

    for i, number in enumerate(leadin_numbers):
        if number != i+1:
            return False

    return True

def extract_title(markdown: str) -> list[str]:
    title = re.findall(r"^#{1} {1}([^\n]+)", markdown)

    if title:
        return title[0]

    raise Exception("Title heading not found in file.\nExpected at least one line to start with '# '.")