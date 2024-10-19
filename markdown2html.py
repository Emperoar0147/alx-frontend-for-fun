#!/usr/bin/python3
import sys
import os
import hashlib

def convert_markdown_to_html_line(line, in_list=False, list_type=None):
    """
    Converts a single line of Markdown text to an HTML line.
    Handles headings, lists, paragraphs, bold, emphasis, and custom cases.
    """
    # Headings (Markdown to HTML: # -> <h1> to <h6>)
    heading_level = 0
    while heading_level < len(line) and line[heading_level] == '#':
        heading_level += 1
    if 1 <= heading_level <= 6:
        heading_text = line[heading_level:].strip()
        return f"<h{heading_level}>{heading_text}</h{heading_level}>\n", False, None

    # Unordered list (-) or Ordered list (*)
    if line.startswith('- ') or line.startswith('* '):
        list_item = line[2:].strip()
        if line.startswith('- '):
            list_tag = 'ul'
        else:
            list_tag = 'ol'
        return f"<li>{list_item}</li>", True, list_tag

    # Bold (**text**) and Emphasis (__text__)
    line = line.replace('**', '<b>').replace('__', '<em>')
    line = line.replace('<b>', '**', 1).replace('<em>', '__', 1)  # Undo accidental replaces

    # Line break inside a paragraph
    if '\n' in line:
        line = line.replace('\n', '<br />\n')

    # MD5 Hash for [[text]]
    if '[[' in line and ']]' in line:
        md5_content = line[line.index('[[') + 2: line.index(']]')]
        md5_hash = hashlib.md5(md5_content.encode()).hexdigest()
        line = line.replace(f'[[{md5_content}]]', md5_hash)

    # Remove 'c' from ((text))
    if '((' in line and '))' in line:
        custom_content = line[line.index('((') + 2: line.index('))')]
        modified_content = custom_content.replace('c', '').replace('C', '')
        line = line.replace(f'(({custom_content}))', modified_content)

    # Return regular paragraph text
    return line, False, None

if __name__ == "__main__":
    # Check the number of arguments
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.exists(markdown_file):
        sys.stderr.write(f"Missing {markdown_file}\n")
        sys.exit(1)

    # Check if the HTML file exists; if not, create it
    if not os.path.exists(html_file):
        with open(html_file, 'w') as new_html_file:
            new_html_file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Default Title</title>\n</head>\n<body>\n")
            new_html_file.write("<p>This is a default content of README.html because the file was missing.</p>\n")
            new_html_file.write("</body>\n</html>\n")
        print(f"{html_file} was missing. A default file has been created.")
    else:
        # Open the Markdown file and read the lines
        with open(markdown_file, 'r') as md_file:
            lines = md_file.readlines()

        in_list = False
        list_type = None

        # Convert each line and write to the HTML file
        with open(html_file, 'w') as html_file:
            for line in lines:
                stripped_line = line.strip()

                if stripped_line == '':
                    continue  # Skip empty lines

                converted_line, is_list, list_tag = convert_markdown_to_html_line(stripped_line, in_list)

                if is_list:
                    # Handle list opening and closing
                    if not in_list:
                        html_file.write(f"<{list_tag}>\n")
                        in_list = True
                        list_type = list_tag
                    html_file.write(converted_line + '\n')
                else:
                    # Handle closing the list
                    if in_list:
                        html_file.write(f"</{list_type}>\n")
                        in_list = False
                        list_type = None
                    html_file.write(f"<p>{converted_line}</p>\n")

            # Close any unclosed list
            if in_list:
                html_file.write(f"</{list_type}>\n")

    sys.exit(0)
