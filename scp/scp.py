import outlines # the best package on earth

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

import json
import os

# Where the entries are stored
scp_dir = "entries"

# Check if folder exists
if not os.path.exists(scp_dir):
    # Make it
    os.makedirs(scp_dir)

class ObjectClass(str, Enum):
    SAFE = "Safe"
    EUCLID = "Euclid"
    KETER = "Keter"
    THAUMIEL = "Thaumiel"
    # Add other classes as needed

class ContainmentProcedures(BaseModel):
    physical_requirements: str
    security_measures: str
    handling_instructions: str
    other_precautions: Optional[str] = None

class Description(BaseModel):
    physical_appearance: Optional[str] = None
    anomalous_properties: str
    origin: Optional[str] = None
    relevant_history: Optional[str] = None

class Addendum(BaseModel):
    title: str
    content: str

class Note(BaseModel):
    content: str

class SCP(BaseModel):
    item_number: str = Field(..., pattern=r"^SCP-\d+$")
    object_class: ObjectClass
    containment_procedures: ContainmentProcedures
    description: Description
    addenda: List[Addendum] = []
    notes: List[Note] = []

    def filepath(self):
        return os.path.join(scp_dir, f"{self.item_number}.txt")

    def save(self):
        # Generate the file path
        file_path = self.filepath()

        # Create the SCP entry text
        scp_text = f"# {self.item_number}\n\n"
        scp_text += f"## Item #: {self.item_number}\n\n"
        scp_text += f"## Object Class: [{self.object_class}]\n\n"
        scp_text += "## Special Containment Procedures:\n\n"
        scp_text += f"{self.containment_procedures.physical_requirements}\n\n"
        scp_text += f"{self.containment_procedures.security_measures}\n\n"
        scp_text += f"{self.containment_procedures.handling_instructions}\n\n"
        if self.containment_procedures.other_precautions:
            scp_text += f"{self.containment_procedures.other_precautions}\n\n"
        scp_text += "## Description:\n\n"
        if self.description.physical_appearance:
            scp_text += f"{self.description.physical_appearance}\n\n"
        scp_text += f"{self.description.anomalous_properties}\n\n"
        if self.description.origin:
            scp_text += f"{self.description.origin}\n\n"
        if self.description.relevant_history:
            scp_text += f"{self.description.relevant_history}\n\n"
        if self.addenda:
            scp_text += "## Addendum:\n\n"
            for addendum in self.addenda:
                scp_text += f"### Addendum {self.item_number}.{self.addenda.index(addendum) + 1}: {addendum.title}\n\n"
                scp_text += f"{addendum.content}\n\n"
        if self.notes:
            scp_text += "## Notes:\n\n"
            for note in self.notes:
                scp_text += f"{note.content}\n\n"

        # Write the SCP entry to the file
        with open(file_path, "w") as file:
            file.write(scp_text)

        print(f"SCP entry saved to {file_path}")

# Using outlines locally
model = outlines.models.transformers(
    "microsoft/Phi-3-mini-128k-instruct",
    device="cpu"
)

# Make the generator
scp_generator = outlines.generate.json(model, SCP)

# Make a new one
entry = scp_generator("Make me an SCP entry.")
entry.save()
print(f"Entry saved to {entry.filepath()}")
