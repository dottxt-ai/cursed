import json
import os
from enum import Enum
from typing import List, Optional

import outlines  # the best package on earth
from classes import SCP, scp_prompt
from pydantic import BaseModel, Field

# Where the entries are stored
scp_dir = "entries"

# Check if folder exists
if not os.path.exists(scp_dir):
    # Make it
    os.makedirs(scp_dir)


# Using outlines locally
model = outlines.models.transformers("microsoft/Phi-3-mini-128k-instruct", device="cpu")

# Make the generator
scp_generator = outlines.generate.json(model, SCP)

# Make a new one
entry = scp_generator(scp_prompt())
entry.save(scp_dir)
print(f"Entry saved to {entry.filepath(scp_dir)}")
