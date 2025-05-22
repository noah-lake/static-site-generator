import os
import shutil

from md_to_html import extract_title, markdown_to_html_node


def copy_static(source, destination):
    if not os.path.exists(source):
        raise ValueError("Source does not exist")
    os.mkdir(destination)
    source_contents = os.listdir(source)
    for c in source_contents:
        path = f"{os.path.join(source)}/{c}"
        mirror = f"{os.path.join(destination)}/{c}"
        if os.path.isdir(path):
            os.mkdir(mirror)
            copy_static(path, mirror)
        if os.path.isfile(path):
            shutil.copy(path, mirror)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as t:
        template = t.read()
    md = markdown_to_html_node(markdown)
    html = md.to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as d:
        d.write(page)


def main():
    shutil.rmtree("/home/noahl/static-site-generator/public")

    copy_static(
        "/home/noahl/static-site-generator/static",
        "/home/noahl/static-site-generator/public",
    )
    # generate_page(
    #    "/home/noahl/static-site-generator/content/index.md",
    #    "/home/noahl/static-site-generator/template.html",
    #    "/home/noahl/static-site-generator/public/index.html",
    # )


main()
