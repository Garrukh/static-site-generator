import unittest
from md_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMdToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading_blocks(self):
        # Valid headings (1 to 6 hash marks followed by a space)
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # Invalid headings (missing space, too many hashes, or leading spaces)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### TooManyHashes"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(" # LeadingSpace"), BlockType.PARAGRAPH)

    def test_code_blocks(self):
        # Valid code blocks (surrounded by 3 backticks and starting with a newline)
        valid_code = "```\ndef my_func():\n    return True\n```"
        self.assertEqual(block_to_block_type(valid_code), BlockType.CODE)
        
        # Invalid code blocks (missing closing backticks, wrong quotes)
        self.assertEqual(block_to_block_type("```python\nprint(1)"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("'''\nprint(1)\n'''"), BlockType.PARAGRAPH)

    def test_quote_blocks(self):
        # Valid quote blocks (every line starts with >)
        single_line_quote = "> This is a quote"
        multi_line_quote = "> Line 1\n> Line 2\n>Line 3"
        self.assertEqual(block_to_block_type(single_line_quote), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(multi_line_quote), BlockType.QUOTE)
        
        # Invalid quote block (one line is missing the > prefix)
        invalid_quote = "> Line 1\nMissing quote mark\n> Line 3"
        self.assertEqual(block_to_block_type(invalid_quote), BlockType.PARAGRAPH)

    def test_unordered_list_blocks(self):
        # Valid unordered lists (every line starts with '- ')
        single_item = "- Item 1"
        multi_item = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(single_item), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(multi_item), BlockType.UNORDERED_LIST)
        
        # Invalid unordered lists (missing space or missing dash on a line)
        self.assertEqual(block_to_block_type("-NoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- Item 1\nItem 2 without dash"), BlockType.PARAGRAPH)

    def test_ordered_list_blocks(self):
        # Valid ordered lists (incrementing integers starting precisely at 1)
        valid_list = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(valid_list), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Only one item"), BlockType.ORDERED_LIST)
        
        # Invalid ordered lists (starts at 2, skips a number, or missing space)
        self.assertEqual(block_to_block_type("2. Starts at two"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. First\n3. Third"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1.First item without space"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. Same\n1. Number"), BlockType.PARAGRAPH)

    def test_paragraph_blocks(self):
        # Standard normal text blocks should default to paragraph
        self.assertEqual(block_to_block_type("Just a normal sentence."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Line one of text.\nLine two of text."), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()