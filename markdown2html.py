#!/usr/bin/python3
import sys
import os

def convert_markdown_to_html_line(line):
    """
    Converts a single line of Markdown text to an HTML line.
    This function handles headings, unordered and ordered lists.
    """
    # Check for heading
    heading_level = 0
    while heading_level < len(line) and line[heading_level] == '#':
        heading_level += 1
    if 1 <= heading_level <= 6:
        heading_text = line[heading_level:].strip()
        return f"<h{heading_level}>{heading_text}</h{heading_level}>\n"

    # Check for unordered list item
    if line.startswith('- '):
        list_item_text = line[2:].strip()
        return f"<li>{list_item_text}</li>\n"

    # Check for ordered list item
    if line.startswith('* '):
        list_item_text = line[2:].strip()
        return f"<li>{list_item_text}</li>\n"

    # Handle normal text (later paragraphs)
    return line

def process_markdown_lines(lines):
    """
    Processes the entire markdown file line by line and converts to HTML.
    Manages unordered and ordered list tags.
    """
    html_lines = []
    inside_ul = False
    inside_ol = False

    for line in lines:
        stripped_line = line.strip()

        # Handle unordered lists
        if stripped_line.startswith('- '):
            if not inside_ul:
                html_lines.append("<ul>\n")
                inside_ul = True
            html_lines.append(convert_markdown_to_html_line(stripped_line))
        else:
            if inside_ul:
                html_lines.append("</ul>\n")
                inside_ul = False

        # Handle ordered lists
        if stripped_line.startswith('* '):
            if not inside_ol:
                html_lines.append("<ol>\n")
                inside_ol = True
            html_lines.append(convert_markdown_to_html_line(stripped_line))
        else:
            if inside_ol:
                html_lines.append("</ol>\n")
                inside_ol = False

        # Handle regular lines
        if not stripped_line.startswith('- ') and not stripped_line.startswith('* '):
            html_lines.append(convert_markdown_to_html_line(stripped_line))

    # Ensure any open lists are closed at the end
    if inside_ul:
        html_lines.append("</ul>\n")
    if inside_ol:
        html_lines.append("</ol>\n")

    return html_lines

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        sys.stderr.write(f"Missing {markdown_file}\n")
        sys.exit(1)

    with open(markdown_file, 'r') as md_file:
        lines = md_file.readlines()

    html_lines = process_markdown_lines(lines)

    with open(html_file, 'w') as html_file:
        html_file.writelines(html_lines)

    sys.exit(0)
