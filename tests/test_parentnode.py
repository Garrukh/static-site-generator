import unittest
from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multi_child_gchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("h1", "grandchild_2")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("a", [grandchild_node, grandchild_node2])
        child_node3 = ParentNode("ul", [grandchild_node2])
        parent_node = ParentNode("div", [child_node, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><a><b>grandchild</b><h1>grandchild_2</h1></a><ul><h1>grandchild_2</h1></ul></div>",
        )

if __name__ == "__main__":
    unittest.main()