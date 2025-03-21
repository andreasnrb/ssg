from enum import Enum

from htmlnode import ParentNode, text_node_to_html_node
from inline_markdown import markdown_to_blocks, text_to_textnodes
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:

    # Check for code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.splitlines()

    if len(lines) == 0:
        return BlockType.PARAGRAPH

    # Check for quote block
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Check for unordered list block
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Check for ordered list block
    if all(line.startswith(str(i) + ". ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST

    # Check for heading
    if (
        lines
        and lines[0].startswith("#")
        and lines[0].find(" ") > 0
        and lines[0].find(" ") <= 7
    ):
        return BlockType.HEADING

    # If none of the above conditions are met, it's a paragraph
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_block = block_to_html_node(block)
        children.append(html_block)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    if len(block) == 0:
        return ParentNode("", [])
    lines = block.split("\n")

    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level == 0 or level > 6:
        raise ValueError(f"invalid heading level: {level}")
    text = block[level:].strip()
    if "#" in text:
        raise ValueError(
            f"invalid heading: #{'#' * level} {text} contains extra '#' characters"
        )
    if not text:
        raise ValueError(f"invalid heading level: {level}")
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    block = block.strip()
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[3:-3]
    text = text.strip()
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
