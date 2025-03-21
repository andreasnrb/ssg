import os
import re


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_title(markdown):
    from blocks import BlockType, block_to_block_type, heading_to_html_node
    from inline_markdown import markdown_to_blocks

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
            if node.tag == "h1":
                return node.children[0].value
    raise ValueError("no title found")


def generate_page(from_path, template_path, dest_path):
    from blocks import markdown_to_html_node

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()
        node = markdown_to_html_node(markdown)
        content = node.to_html()
        title = extract_title(markdown)
    with open(template_path, "r") as file:
        template = file.read()

    file_content = template.replace("{{ Title }}", title)
    file_content = file_content.replace("{{ Content }}", content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(file_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    file_paths = []
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            file_paths.append(os.path.join(root, file))

    for file in file_paths:
        new_file = os.path.splitext(file)[0] + ".html"
        new_file = new_file.replace(dir_path_content, dest_dir_path)
        generate_page(
            file,
            template_path + "/template.html",
            new_file,
        )
