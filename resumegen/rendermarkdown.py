#!/usr/bin/env python3.8

import argparse
import json
from datetime import date

def block_date(block):
    if 'startDate' in block and block['startDate']:
        if 'endDate' in block and block['endDate']:
            return f"{block['startDate']} - {block['endDate']}"
        else:
            return f"{block['startDate']} - Present"
    return ""

def block_header(block, name_key):
    if 'url' in block and block['url']:
        return f"[{block[name_key]}]({block['url']})"
    return block[name_key]

if __name__ == '__main__':
    parser = argparse.ArgumentParser("rendermarkdown")
    parser.add_argument("input", type=str)
    parser.add_argument("out", type=str)
    parser.add_argument("--include_basics", action="store_true")

    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = json.loads(f.read())

    with open(args.out, "w") as f:
        if args.include_basics:
            f.write(f"# {data['name']}\n")
            f.write(f"\n{data['label']}\n")
            f.write(f"\nEmail: {data['email']}\n")
            f.write(f"\nWebsite: {data['url']}\n")
        f.write(f"## Education\n")
        for block in data['education']:
            f.write(f"### {block_header(block, 'institution')}\n")
            f.write(f"\n{block_date(block)}\n")
            f.write(f"\n{block['area']} - {block['score']}\n")
            if 'highlights' in block:
                for highlight in block['highlights']:
                    f.write(f"* {highlight}\n")
            f.write("\n\n")
        f.write(f"## Work\n")
        for block in data['work']:
            f.write(f"### {block_header(block, 'company')}\n")
            f.write(f"\n{block_date(block)}\n")
            f.write(f"\n{block['summary']}\n")
            if 'highlights' in block:
                for highlight in block['highlights']:
                    f.write(f"* {highlight}\n")
            f.write("\n\n")
        f.write(f"## Projects\n")
        for block in data['projects']:
            f.write(f"### {block_header(block, 'name')}\n")
            f.write(f"\n{block_date(block)}\n")
            f.write(f"\n{block['description']}\n")
            if 'highlights' in block:
                for highlight in block['highlights']:
                    f.write(f"* {highlight}\n")
            f.write("\n\n")
