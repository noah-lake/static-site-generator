import os
import shutil

from md_to_html import extract_title, markdown_to_html_node


def copy_static(source, destination):
    if not os.path.exists(source):
        raise ValueError("Source does not exist")
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
    # if not os.path.exists(dest_path):
    # os.makedirs(dest_path)
    with open(dest_path, "w") as d:
        d.write(page)


def main():
    for f in os.listdir("./public"):
        filepath = os.path.join("./public", f)
        os.remove(filepath)

    copy_static(
        "./static",
        "./public",
    )


#    generate_page(
#        "./content/index.md",
#        "./template.html",
#        "./public/index.html",
#    )


main()
