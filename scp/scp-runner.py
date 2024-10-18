import outlines
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import json
import os
from datetime import datetime

from api import create_completion
from classes import SCP, Reviewer, reviewer_prompt, scp_prompt

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

# Review it
review = create_completion(Reviewer, reviewer_prompt(entry))

# Save it to disk
review_path = os.path.join(review_dir, f"{entry.item_number}.txt")
review.save(review_path)
print(f"Review saved to {review_path}")

# Generate an index.html file
index_file = os.path.join(scp_dir, "index.html")
entries = [f for f in os.listdir(scp_dir) if f.endswith(".txt")]
entry_names = [f.replace(".txt", "") for f in entries]

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCP Entries Index</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }}
        h1 {{ color: #333; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin-bottom: 10px; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>SCP Entries Index</h1>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <ul>
        {"".join(f'<li><a href="{entry}">{entry_name}</a></li>' for entry_name, entry in sorted(zip(entry_names, entries), key=lambda x: x[0]))}
    </ul>
</body>
</html>
"""

with open(index_file, "w") as f:
    f.write(html_content)

print(f"Index file updated: {index_file}")
