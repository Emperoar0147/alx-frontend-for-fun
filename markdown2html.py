#!/usr/bin/python3
import sys
import os

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the input Markdown file exists
    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        exit(1)
    
    # Read content from the Markdown file and write it to the HTML file
    try:
        with open(input_file, 'r') as md_file:
            content = md_file.read()

        with open(output_file, 'w') as html_file:
            html_file.write(content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(1)

    # Exit with 0 status on successful execution
    exit(0)
