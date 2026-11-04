from enum import Enum
from regex import is_heading_block, is_code_block, is_quote_block, is_unordered_block, is_ordered_list_block

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")

    for i, block in enumerate(blocks):
        blocks[i] = block.strip()

    return list(filter(lambda a: a != '', blocks))

def block_to_block_type(block: str) -> BlockType:
    if is_heading_block(block):
        return BlockType.HEADING

    if is_code_block(block):
        return BlockType.CODE

    if is_quote_block(block):
        return BlockType.QUOTE

    if is_unordered_block(block):
        return BlockType.UNORDERED_LIST

    if is_ordered_list_block(block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH