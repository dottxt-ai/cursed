"""
If you want to make this code less hideous, please do!

part of the curse is the ugly code

- cameron
"""

import os

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ObjectClass(str, Enum):
    SAFE = "Safe"
    EUCLID = "Euclid"
    KETER = "Keter"
    THAUMIEL = "Thaumiel"
    # Add other classes as needed

class ContainmentProcedures(BaseModel):
    physical_requirements: str = Field(..., description="Physical requirements for containing the SCP")
    security_measures: str = Field(..., description="Security measures required for the SCP")
    handling_instructions: str = Field(..., description="Instructions for handling the SCP")
    other_precautions: Optional[str] = Field(None, description="Additional precautions if necessary")

class Description(BaseModel):
    physical_appearance: Optional[str] = Field(None, description="Physical description of the SCP")
    anomalous_properties: str = Field(..., description="Anomalous properties of the SCP")
    origin: Optional[str] = Field(None, description="Origin of the SCP, if known")
    relevant_history: Optional[str] = Field(None, description="Relevant historical information about the SCP")

class Addendum(BaseModel):
    title: str = Field(..., description="Title of the addendum")
    content: str = Field(..., description="Content of the addendum")

class Note(BaseModel):
    content: str = Field(..., description="Content of the note")

class SCP(BaseModel):
    item_number: str = Field(..., pattern=r"^SCP-\d+$", description="Unique identifier for the SCP")
    object_class: ObjectClass = Field(..., description="Classification of the SCP's containment difficulty")
    containment_procedures: ContainmentProcedures = Field(..., description="Procedures for containing the SCP")
    description: Description = Field(..., description="Detailed description of the SCP")
    addenda: List[Addendum] = Field(default_factory=list, description="Additional information about the SCP")
    notes: List[Note] = Field(default_factory=list, description="Miscellaneous notes about the SCP")

    def filepath(self, scp_dir):
        return os.path.join(scp_dir, f"{self.item_number}.txt")

    def save(self, scp_dir):
        # Generate the file path
        file_path = self.filepath(scp_dir)

        # Check for existing files with the same SCP number
        if os.path.exists(file_path):
            existing_files = [f for f in os.listdir(scp_dir) if f.startswith("SCP-")]
            existing_numbers = [int(f.split("-")[1].split(".")[0]) for f in existing_files]
            new_number = max(existing_numbers) + 1
            old_number = self.item_number
            self.item_number = f"SCP-{new_number:03d}"
            file_path = os.path.join(scp_dir, f"{self.item_number}.txt")

            # Update all fields containing the old SCP number
            for field in self.model_fields.values():
                if isinstance(getattr(self, field.name), str):
                    setattr(self, field.name, getattr(self, field.name).replace(old_number, self.item_number))
                elif isinstance(getattr(self, field.name), list):
                    for i, item in enumerate(getattr(self, field.name)):
                        if isinstance(item, BaseModel):
                            for sub_field in item.model_fields.values():
                                if isinstance(getattr(item, sub_field.name), str):
                                    setattr(item, sub_field.name, getattr(item, sub_field.name).replace(old_number, self.item_number))
                        elif isinstance(item, str):
                            getattr(self, field.name)[i] = item.replace(old_number, self.item_number)

        # Create the SCP entry text
        scp_text = f"# {self.item_number}\n\n"
        scp_text += f"## Item #: {self.item_number}\n\n"
        scp_text += f"## Object Class: [{self.object_class}]\n\n"

        # Add the containment procedures
        scp_text += "## Special Containment Procedures\n\n"

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
            for index, addendum in enumerate(self.addenda, start=1):
                scp_text += f"### Addendum {self.item_number}.{index}: {addendum.title}\n\n"
                scp_text += f"{addendum.content}\n\n"
        if self.notes:
            scp_text += "## Notes:\n\n"
            for note in self.notes:
                scp_text += f"{note.content}\n\n"

        # Write the SCP entry to the file
        with open(file_path, "w") as file:
            file.write(scp_text)

        print(f"SCP entry saved to {file_path}")

def scp_prompt() -> str:
    # Make the JSON schema
    json_schema = SCP.model_json_schema()

    return f"""
    <|im_start|>system
    Your role is to create SCP entries. An SCP entry is a document that
    describes an anomalous object, phenomenon, or entity, and the procedures
    and precautions that must be taken to contain it.

    You must provide

    - An SCP number in the format SCP-[number]
    - The object class of the SCP, which is one of the following: Safe, Euclid, Keter, or Thaumiel
    - The special containment procedures for the SCP. Be detailed and specific. A reader of this
      SCP entry should be able to contain the SCP without any ambiguity. SCP entities may be dangerous
      or require special handling, and so the containment procedures are of the utmost importance.
    - The description of the SCP, including its physical appearance, anomalous properties,
      origin, and relevant history.
    - Any addenda to the SCP, which are additional documents that provide more information about the SCP.
      Addenda are optional, but can help provide more context about the SCP and its anomalies. Addenda
      typically come in the form of documents, logs, or other records that provide more information about
      the history of the SCP's acquisition, experimentation, and any other important information.
    - Any notes that are relevant to the SCP. Notes are optional, and can provide additional information
      about the SCP that is not covered elsewhere. Notes can be used to provide speculation, theorizing,
      or other information that is relevant to the SCP.

    You must provide all the above fields in valid JSON. Your schema is:

    ```json
    {json_schema}
    ```

    <|im_end|>
    <|im_start|>user

    Please produce an SCP entry.

    <|im_end|>
    <|im_start|>assistant
    """
