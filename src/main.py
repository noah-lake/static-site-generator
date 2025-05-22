import os
import shutil
import sys
from md_to_html import extract_title, markdown_to_html_node


def copy_static(source, destination):
    """Copies all contents of one directory into another. Accepts two filepaths as inputs"""
    if not os.path.exists(source):
        raise ValueError("Source does not exist")
    source_contents = os.listdir(source)  # Returns a list of directory and file names
    for f in source_contents:
        # Make some similar filepaths
        path = f"{os.path.join(source)}/{f}"
        mirror = f"{os.path.join(destination)}/{f}"
        # If the path is a directory, make an identical directory in destination and recur
        if os.path.isdir(path):
            os.mkdir(mirror)
            copy_static(path, mirror)
        # If the path is a file, copy it into destination
        if os.path.isfile(path):
            shutil.copy(path, mirror)


def generate_page(from_path, template_path, dest_path, basepath):
    """Takes data from a .md file at from_path and converts it into a .html page (assuming that template_path points to a .html) at dest_path."""
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as t:
        template = t.read()
    # Convert the file's markdown data into a single ParentNode object
    md = markdown_to_html_node(markdown)
    # Translate the parent node into a string of HTML formatted text
    html = md.to_html()
    title = extract_title(markdown)
    # Copy a template file (a .html in this case) and replace its filler content with our html data
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    formatted_page = page.replace('href="/', f'href="{basepath}').replace(
        'src="/', f'src="{basepath}'
    )
    # Write it to destination
    with open(dest_path, "w") as d:
        d.write(formatted_page)


def generate_pages_recursive(dir_path, template_path, dest_dir_path, basepath):
    """Crawls through a parent directory to generate pages for all files inside using generate_page()"""
    contents = os.listdir(dir_path)
    for f in contents:
        # Paths to keep track of where we are in each directory
        path = f"{os.path.join(dir_path)}/{f}"
        mirror = f"{os.path.join(dest_dir_path)}/{f}"
        # If the path is a director, make sure mirror has the same directory, then recur
        if os.path.isdir(path):
            os.makedirs(mirror, exist_ok=True)
            generate_pages_recursive(path, template_path, mirror, basepath)
        if os.path.isfile(path):
            # If the path is a file, step back into the directory and point to a file called index.html, then generate_page()
            # Because of the hardcoded nature of where the path points towards, you cannot have more than one file in each dir_path directory
            goal = f"{os.path.join(dest_dir_path)}/index.html"
            generate_page(path, template_path, goal, basepath)


def main(basepath="/"):
    # Removes the contents of the docs folder for regeneration
    for f in os.listdir("docs"):
        filepath = os.path.join("docs", f)
        if os.path.isfile(filepath):
            os.remove(filepath)
        if os.path.isdir(filepath):
            shutil.rmtree(filepath)

    # Copies all of the static data into docs
    copy_static(
        "static",
        "docs",
    )

    # Generates pages for each file in the content directory and writes them into docs
    generate_pages_recursive(
        dir_path="content",
        template_path="template.html",
        dest_dir_path="docs",
        basepath=basepath,
    )


# Tries to take an argument from the cli, defaults to "/" if none is provided
try:
    basepath = sys.argv[1]
except IndexError:
    basepath = "/"
main(basepath)
