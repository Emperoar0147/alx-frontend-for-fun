#!/usr/bin/python3

import sys
import os


def print_usage_and_exit():
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)


def check_file_exists(file_name):
    if not os.path.isfile(file_name):
        print(f"Missing {file_name}", file=sys.stderr)
        sys.exit(1)


def convert_markdown_to_html_line(line, in_list):
    stripped_line = line.strip()

    if stripped_line.startswith('#'):
        level = stripped_line.count('#')
        heading = stripped_line[level:].strip()
        return (
            f"<h{level}>{heading}</h{level}>",
            False,
            in_list
        )

    elif stripped_line.startswith('- '):
        list_item = stripped_line[2:].strip()
        if not in_list:
            in_list = True
            return (
                f"<ul>\n<li>{list_item}</li>",
                True,
                in_list
            )
        else:
            return f"<li>{list_item}</li>", True, in_list

    elif stripped_line.startswith('* '):
        list_item = stripped_line[2:].strip()
        if not in_list:
            in_list = True
            return (
                f"<ol>\n<li>{list_item}</li>",
                True,
                in_list
            )
        else:
            return f"<li>{list_item}</li>", True, in_list

    elif stripped_line == '':
        return None, False, in_list

    else:
        if in_list:
            if line.startswith('- '):
                return "</ul>", False, False
            elif line.startswith('* '):
                return "</ol>", False, False

        return f"<p>{stripped_line}</p>", False, in_list


def convert_markdown_to_html(input_file, output_file):
    check_file_exists(input_file)

    with open(input_file, 'r') as md_file:
        lines = md_file.readlines()

    in_list = False
    html_content = []

    for line in lines:
        converted_line, is_list, in_list = convert_markdown_to_html_line(
            line, in_list
        )

        if converted_line:
            html_content.append(converted_line)

    if in_list:
        if line.startswith('- '):
            html_content.append("</ul>")
        elif line.startswith('* '):
            html_content.append("</ol>")

    with open(output_file, 'w') as html_file:
        html_file.write('\n'.join(html_content))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage_and_exit()

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(markdown_file, output_file)
