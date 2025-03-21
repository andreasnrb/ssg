from helpers import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        images = extract_markdown_images(old_node.text)
        temp = old_node.text
        for alt, src in images:
            texts = temp.split(f"![{alt}]({src})", 1)
            if len(texts[0]) > 0:
                split_nodes.append(TextNode(texts[0], TextType.TEXT))
            split_nodes.append(TextNode(alt, TextType.IMAGE, src))
            if len(texts) > 0:
                temp = texts[len(texts) - 1]
        if len(temp) > 0:
            split_nodes.append(TextNode(temp, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        links = extract_markdown_links(old_node.text)
        temp = old_node.text
        for text, href in links:
            texts = temp.split(f"[{text}]({href})", 1)
            if len(texts[0]) > 0:
                split_nodes.append(TextNode(texts[0], TextType.TEXT))
            split_nodes.append(TextNode(text, TextType.LINK, href))
            if len(texts) > 0:
                temp = texts[len(texts) - 1]
        if len(temp) > 0:
            split_nodes.append(TextNode(temp, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes


def markdown_to_blocks(markdown):
    splited = markdown.split("\n\n")
    return [s.strip() for s in splited]
