import unittest
from inline_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestMdToNode(unittest.TestCase):
    def test_plain_text(self):
        case = split_nodes_delimiter([TextNode("This is a text node", TextType.TEXT)], "**", TextType.BOLD)
        expected_result = [TextNode("This is a text node", TextType.TEXT)]
        self.assertEqual(case, expected_result)

    def test_bold(self):
        case = split_nodes_delimiter([TextNode("**This** is a text with bold **marked**", TextType.TEXT)], "**", TextType.BOLD)
        expected_result = [TextNode("This", TextType.BOLD), TextNode(" is a text with bold ", TextType.TEXT), TextNode("marked", TextType.BOLD)]
        self.assertEqual(case, expected_result)

    def test_code(self):
        case = split_nodes_delimiter([TextNode("`This` is a text with code `marked`", TextType.TEXT)], "`", TextType.CODE)
        expected_result = [TextNode("This", TextType.CODE), TextNode(" is a text with code ", TextType.TEXT), TextNode("marked", TextType.CODE)]
        self.assertEqual(case, expected_result)

    def test_nontext_node(self):
        case = split_nodes_delimiter([TextNode("This is **not** a text node", TextType.ITALIC)], "**", TextType.BOLD)
        expected_result = [TextNode("This is **not** a text node", TextType.ITALIC)]
        self.assertEqual(case, expected_result)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_images_not_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a link [to boot dev](https://www.boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_not_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_full_interpretation(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK ,"https://boot.dev"),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()