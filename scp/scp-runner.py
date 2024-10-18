import outlines # the best package on earth

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

import json
import os

from api import create_completion
from classes import SCP, scp_prompt

# Where the entries are stored
scp_dir = "entries"

# Check if folder exists
if not os.path.exists(scp_dir):
    # Make it
    os.makedirs(scp_dir)

# Call the api
entry = create_completion(SCP, scp_prompt())

# Save it to disk
entry.save(scp_dir)
print(f"Entry saved to {entry.filepath(scp_dir)}")