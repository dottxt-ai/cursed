import json
import os
from datetime import datetime
from enum import Enum
from typing import List, Optional

from api import create_completion
from classes import SCP, Reviewer, apply_scp_theme, reviewer_prompt, scp_prompt
from pydantic import BaseModel, Field

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

# Check if the entry already exists
if os.path.exists(entry.filepath(scp_dir)) or os.path.exists(entry.html_filepath(scp_dir)):
    print(f"Entry {entry.item_number} already exists. Skipping.")
else:
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

print("SCP entry generation complete.")
