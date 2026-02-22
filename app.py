import sys
import os
import re
import json
import markdown
from flask import Flask, render_template

app = Flask(__name__)
MD_FILE = "example.md"

def parse_param_string(param_str):
    """
    Parses a string like: 
    name="Machine ID" type=text enabled=true options=[a,b,c]
    into a Python dictionary.
    """
    # Regex to capture key="value", key=[list], or key=value
    pattern = re.compile(r'(\w+)=(?:\[(.*?)\]|"(.*?)"|([^\s\}]+))')
    
    params = {}
    for match in pattern.finditer(param_str):
        key = match.group(1)
        list_val = match.group(2)
        quote_val = match.group(3)
        raw_val = match.group(4)

        if list_val is not None:
            # Convert "a,b,c" to ["a", "b", "c"]
            params[key] = [x.strip() for x in list_val.split(',')] if list_val.strip() else []
        elif quote_val is not None:
            params[key] = quote_val
        else:
            # Handle booleans and numbers
            if raw_val.lower() == 'true': params[key] = True
            elif raw_val.lower() == 'false': params[key] = False
            else: params[key] = raw_val
            
    return params

def parse_markdown_to_structure(filepath):
    if not os.path.exists(filepath):
        return {"categories": []}

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    categories = []
    current_cat = None   # H1
    current_item = None  # H2
    current_card = None  # H3

    # Regex patterns
    h1_re = re.compile(r'^#\s+(.+)')
    h2_re = re.compile(r'^##\s+(.+)')
    h3_re = re.compile(r'^###\s+(.+)')
    # Param regex: @param varName { ... }
    param_re = re.compile(r'^@param\s+(\w+)\s+\{(.+)\}')

    for line in lines:
        line = line.rstrip()
        
        # 1. Check for Parameters first
        p_match = param_re.match(line)
        if p_match:
            p_id = p_match.group(1)
            p_config = parse_param_string(p_match.group(2))
            p_config['id'] = p_id # Add ID to config
            
            # Decide scope: Card (H3) or Item (H2)
            if current_card:
                current_card['params'].append(p_config)
            elif current_item:
                current_item['params'].append(p_config)
            continue # Skip rendering this line

        # 2. Check Headers
        m1 = h1_re.match(line)
        if m1:
            current_cat = { "title": m1.group(1), "items": [], "defaultExpanded": False }
            categories.append(current_cat)
            current_item = None
            current_card = None
            continue

        m2 = h2_re.match(line)
        if m2:
            if not current_cat:
                current_cat = {"title": "General", "items": [], "defaultExpanded": False}
                categories.append(current_cat)
            
            current_item = { "name": m2.group(1), "cards": [], "params": [] }
            current_cat['items'].append(current_item)
            current_card = None
            continue

        m3 = h3_re.match(line)
        if m3:
            if not current_item:
                 # safety fallback
                 if not current_cat: categories.append({"title": "General", "items": []})
                 current_item = {"name": "Overview", "cards": [], "params": []}
                 categories[-1]['items'].append(current_item)

            current_card = { "title": m3.group(1), "content_raw": [], "params": [] }
            current_item['cards'].append(current_card)
            continue

        # 3. Content
        if line or (current_card and current_card['content_raw']):
            if current_item and not current_card:
                # Create default card if content exists before H3
                current_card = {"title": "Intro", "content_raw": [], "params": []}
                current_item['cards'].append(current_card)
            
            if current_card:
                current_card['content_raw'].append(line)

    # Convert Markdown to HTML
    md = markdown.Markdown(extensions=['fenced_code', 'codehilite'])
    for cat in categories:
        for item in cat['items']:
            for card in item['cards']:
                raw_text = "\n".join(card['content_raw'])
                card['html'] = md.convert(raw_text)

    return {"categories": categories}

@app.route('/')
def index():
    data = parse_markdown_to_structure(MD_FILE)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        MD_FILE = sys.argv[1]

    port = 5000
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print(f"Warning: Invalid port number '{sys.argv[2]}'. Using default 5000.", file=sys.stderr)

    app.run(debug=True, port=port)