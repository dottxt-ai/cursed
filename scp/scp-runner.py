import outlines
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import json
import os
from datetime import datetime

from api import create_completion
from classes import SCP, Reviewer, apply_scp_theme, reviewer_prompt, scp_prompt

# Where the entries are stored
scp_dir = "entries"
review_dir = "entries/reviews"

# Check if entries and reviews folders exist
dirs = [scp_dir, review_dir]
for dir in dirs:
    if not os.path.exists(dir):
        # Make it
        os.makedirs(dir)


# Call the api
entry = create_completion(SCP, scp_prompt())

# Save it to disk
entry.save(scp_dir)
print(f"Entry saved to {entry.filepath(scp_dir)}")

# Save the entry to HTML
html_content = entry.to_html()
html_path = entry.html_filepath(scp_dir)
with open(html_path, "w") as f:
    f.write(html_content)
print(f"HTML saved to {html_path}")

# Review it
review = create_completion(Reviewer, reviewer_prompt(entry))

# Save it to disk
review_path = os.path.join(review_dir, f"{entry.item_number}.txt")
review.save(review_path)
print(f"Review saved to {review_path}")

# Generate an index.html file
index_file = os.path.join(scp_dir, "index.html")
entries = [f for f in os.listdir(scp_dir) if f.endswith(".html") and f != "index.html"]
entry_names = [f.replace(".html", "") for f in entries]

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCP Foundation - Secure, Contain, Protect</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            line-height: 1.6;
            padding: 20px;
            background-color: #f0f0f0;
            color: #333;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #990000;
            text-align: center;
            border-bottom: 2px solid #990000;
            padding-bottom: 10px;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
        }}
        li {{
            margin-bottom: 10px;
            padding: 10px;
            background-color: #f9f9f9;
            border-left: 3px solid #990000;
        }}
        a {{
            color: #990000;
            text-decoration: none;
            font-weight: bold;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .update-info {{
            text-align: right;
            font-style: italic;
            margin-top: 20px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>SCP Foundation Archives</h1>
        <ul>
            {"".join(f'<li><a href="{entry}">{entry_name}</a></li>' for entry_name, entry in sorted(zip(entry_names, entries), key=lambda x: x[0]))}
        </ul>
        <p class="update-info">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>
"""

with open(index_file, "w") as f:
    f.write(html_content)

print(f"Index file updated: {index_file}")
