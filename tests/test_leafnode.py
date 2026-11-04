import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_no_tag(self):
        node = LeafNode("", "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_values(self):
        node = LeafNode("p", "Hello, world!", {"hey": "there"})
        self.assertEqual(
            node.tag,
            "p"
        )
        self.assertEqual(
            node.value,
            "Hello, world!"
        )
        self.assertEqual(
            node.props,
            {"hey": "there"}
        )

if __name__ == "__main__":
    unittest.main()