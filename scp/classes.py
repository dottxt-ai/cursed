"""
If you want to make this code less hideous, please do!

part of the curse is the ugly code

- cameron
"""

import os
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


# This is used to guide the model to produce the correct type of SCP entry
class EntryType(str, Enum):
    # Sentient Entities
    HUMAN = "Human"
    HUMANOID = "Humanoid"
    NON_HUMANOID_INTELLIGENT = "Non-Humanoid Intelligent"
    ARTIFICIAL_INTELLIGENCE = "Artificial Intelligence"
    HIVE_MIND = "Hive Mind"

    # Non-Sentient Creatures
    ANIMAL = "Animal"
    PLANT = "Plant"
    FUNGUS = "Fungus"
    MICROORGANISM = "Microorganism"
    EXTINCT_CREATURE = "Extinct or Prehistoric Creature"

    # Objects
    ARTIFACT = "Artifact"
    TOOL = "Tool"
    WEAPON = "Weapon"
    MACHINERY = "Machinery"
    ART_PIECE = "Art Piece"
    BOOK_OR_DOCUMENT = "Book or Document"

    # Locations
    BUILDING = "Building"
    GEOGRAPHICAL_FEATURE = "Geographical Feature"
    ECOSYSTEM = "Ecosystem"
    POCKET_DIMENSION = "Pocket Dimension"
    ALTERNATE_REALITY = "Alternate Reality"

    # Phenomena
    NATURAL_PHENOMENON = "Natural Phenomenon"
    SUPERNATURAL_OCCURRENCE = "Supernatural Occurrence"
    PHYSICAL_LAW = "Physical Law or Constant"
    TEMPORAL_ANOMALY = "Temporal Anomaly"
    SPATIAL_ANOMALY = "Spatial Anomaly"

    # Events
    RECURRING_EVENT = "Recurring Event"
    ONE_TIME_OCCURRENCE = "One-Time Occurrence"
    RITUAL = "Ritual"
    PROPHECY = "Prophecy"

    # Concepts
    ABSTRACT_IDEA = "Abstract Idea"
    MEMETIC_HAZARD = "Memetic Hazard"
    INFOHAZARD = "Infohazard"
    COGNITOHAZARD = "Cognitohazard"

    # Materials
    SUBSTANCE = "Substance"
    COMPOUND = "Compound"
    ELEMENT = "Element"
    EXOTIC_MATTER = "Exotic Matter"

    # Energy Forms
    RADIATION = "Radiation"
    FIELD = "Field"
    WAVE = "Wave"

    # Psychological
    MENTAL_STATE = "Mental State"
    EMOTIONAL_CONDITION = "Emotional Condition"
    ALTERED_PERCEPTION = "Altered Perception"

    # Biological
    DISEASE = "Disease"
    MUTATION = "Mutation"
    SYMBIOTE = "Symbiote"
    PARASITE = "Parasite"

    # Technological
    ADVANCED_TECH = "Advanced Technology"
    ANOMALOUS_SOFTWARE = "Anomalous Software"
    REALITY_ALTERING_DEVICE = "Reality-Altering Device"

    # Extradimensional
    EXTRADIMENSIONAL_BEING = "Extradimensional Being"
    PORTAL = "Portal"
    OVERLAPPING_REALITY = "Overlapping Reality"

    # Cosmic
    CELESTIAL_BODY = "Celestial Body"
    SPACE_TIME_ANOMALY = "Space-Time Anomaly"
    UNIVERSAL_CONSTANT = "Universal Constant"

    # Temporal
    TIME_LOOP = "Time Loop"
    ALTERNATE_TIMELINE = "Alternate Timeline"
    PRECOGNITION_RETROCOGNITION = "Precognition/Retrocognition Effect"

    # Social
    ORGANIZATION = "Organization"
    CULTURE = "Culture"
    BELIEF_SYSTEM = "Belief System"

    # Meta
    SELF_REFERENTIAL = "Self-Referential SCP"
    DOCUMENTATION_AFFECTING = "Documentation-Affecting SCP"
    REALITY_BENDING_NARRATIVE = "Reality-Bending Narrative Element"


class ObjectClass(str, Enum):
    SAFE = "Safe"
    EUCLID = "Euclid"
    KETER = "Keter"
    THAUMIEL = "Thaumiel"
    # Add other classes as needed


class ContainmentProcedures(BaseModel):
    physical_requirements: str = Field(
        ..., description="Physical requirements for containing the SCP"
    )
    security_measures: str = Field(
        ..., description="Security measures required for the SCP"
    )
    handling_instructions: str = Field(
        ..., description="Instructions for handling the SCP"
    )
    other_precautions: Optional[str] = Field(
        None, description="Additional precautions if necessary"
    )


class Description(BaseModel):
    physical_appearance: Optional[str] = Field(
        None, description="Physical description of the SCP"
    )
    anomalous_properties: str = Field(
        ..., description="Anomalous properties of the SCP"
    )
    origin: Optional[str] = Field(None, description="Origin of the SCP, if known")
    relevant_history: Optional[str] = Field(
        None, description="Relevant historical information about the SCP"
    )


class Addendum(BaseModel):
    title: str = Field(..., description="Title of the addendum")
    content: str = Field(..., description="Content of the addendum")


class Note(BaseModel):
    content: str = Field(..., description="Content of the note")


class SCP(BaseModel):
    entry_type: EntryType = Field(..., description="Type of the SCP entry")
    item_number: str = Field(
        ..., pattern=r"^SCP-\d+$", description="Unique identifier for the SCP"
    )
    object_class: ObjectClass = Field(
        ..., description="Classification of the SCP's containment difficulty"
    )

    # Putting description here because it guides the rest of the generation
    description: Description = Field(..., description="Detailed description of the SCP")
    containment_procedures: ContainmentProcedures = Field(
        ..., description="Procedures for containing the SCP"
    )
    addenda: List[Addendum] = Field(
        default_factory=list, description="Additional information about the SCP"
    )
    notes: List[Note] = Field(
        default_factory=list, description="Miscellaneous notes about the SCP"
    )

    def filepath(self, scp_dir):
        return os.path.join(scp_dir, f"{self.item_number}.txt")

    def html_filepath(self, scp_dir):
        return os.path.join(scp_dir, f"{self.item_number}.html")

    def __str__(self):
        content = f"""
# {self.item_number}

**Object Class:** {self.object_class}
**Entry Type:** {self.entry_type}

## Special Containment Procedures

- **Physical Requirements:** {self.containment_procedures.physical_requirements}
- **Security Measures:** {self.containment_procedures.security_measures}
- **Handling Instructions:** {self.containment_procedures.handling_instructions}
"""

        if self.containment_procedures.other_precautions:
            content += f"- **Additional Precautions:** {self.containment_procedures.other_precautions}\n"

        content += "\n## Description\n\n"

        if self.description.physical_appearance:
            content += (
                f"**Physical Appearance:** {self.description.physical_appearance}\n\n"
            )

        content += (
            f"**Anomalous Properties:** {self.description.anomalous_properties}\n\n"
        )

        if self.description.origin:
            content += f"**Origin:** {self.description.origin}\n\n"

        if self.description.relevant_history:
            content += f"**Relevant History:** {self.description.relevant_history}\n\n"

        if self.addenda:
            content += "## Addenda\n\n"
            for index, addendum in enumerate(self.addenda, start=1):
                content += (
                    f"### Addendum {self.item_number}.{index}: {addendum.title}\n\n"
                )
                content += f"{addendum.content}\n\n"

        if self.notes:
            content += "## Notes\n\n"
            for note in self.notes:
                content += f"- {note.content}\n"

        return content.strip()

    def save(self, scp_dir):
        # Generate the file path
        file_path = self.filepath(scp_dir)

        # Check for existing files with the same SCP number
        if os.path.exists(file_path):
            existing_files = [f for f in os.listdir(scp_dir) if f.startswith("SCP-")]
            existing_numbers = [
                int(f.split("-")[1].split(".")[0]) for f in existing_files
            ]
            new_number = max(existing_numbers) + 1
            old_number = self.item_number
            self.item_number = f"SCP-{new_number:03d}"
            file_path = os.path.join(scp_dir, f"{self.item_number}.txt")

            # Update all fields containing the old SCP number
            for field_name, field in self.model_fields.items():
                value = getattr(self, field_name)
                if isinstance(value, str):
                    setattr(
                        self, field_name, value.replace(old_number, self.item_number)
                    )
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        if isinstance(item, BaseModel):
                            for sub_field_name, sub_field in item.model_fields.items():
                                sub_value = getattr(item, sub_field_name)
                                if isinstance(sub_value, str):
                                    setattr(
                                        item,
                                        sub_field_name,
                                        sub_value.replace(old_number, self.item_number),
                                    )
                        elif isinstance(item, str):
                            value[i] = item.replace(old_number, self.item_number)

        # Write the SCP entry to the file
        with open(file_path, "w") as file:
            file.write(str(self))

    def to_html(self):
        content = f"""
        <h1>{self.item_number}</h1>
        <p><strong>Object Class:</strong> {self.object_class}</p>
        <p><strong>Entry Type:</strong> {self.entry_type}</p>

        <h2>Special Containment Procedures</h2>
        <ul>
            <li><strong>Physical Requirements:</strong> {self.containment_procedures.physical_requirements}</li>
            <li><strong>Security Measures:</strong> {self.containment_procedures.security_measures}</li>
            <li><strong>Handling Instructions:</strong> {self.containment_procedures.handling_instructions}</li>
        """

        if self.containment_procedures.other_precautions:
            content += f"<li><strong>Additional Precautions:</strong> {self.containment_procedures.other_precautions}</li>"

        content += "</ul>"

        content += "<h2>Description</h2>"

        if self.description.physical_appearance:
            content += f"<p><strong>Physical Appearance:</strong> {self.description.physical_appearance}</p>"

        content += f"<p><strong>Anomalous Properties:</strong> {self.description.anomalous_properties}</p>"

        if self.description.origin:
            content += f"<p><strong>Origin:</strong> {self.description.origin}</p>"

        if self.description.relevant_history:
            content += f"<p><strong>Relevant History:</strong> {self.description.relevant_history}</p>"

        if self.addenda:
            content += "<h2>Addenda</h2>"
            for index, addendum in enumerate(self.addenda, start=1):
                content += (
                    f"<h3>Addendum {self.item_number}.{index}: {addendum.title}</h3>"
                )
                content += f"<p>{addendum.content}</p>"

        if self.notes:
            content += "<h2>Notes</h2><ul>"
            for note in self.notes:
                content += f"<li>{note.content}</li>"
            content += "</ul>"

        return apply_scp_theme(content)


def apply_scp_theme(content):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SCP Foundation - {content.split('<h1>')[1].split('</h1>')[0]}</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            .container {{
                background-color: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            h1, h2, h3 {{
                color: #990000;
            }}
            h1 {{
                text-align: center;
                border-bottom: 2px solid #990000;
                padding-bottom: 10px;
            }}
            ul {{
                list-style-type: none;
                padding-left: 0;
            }}
            li {{
                margin-bottom: 10px;
                padding: 10px;
                background-color: #f9f9f9;
                border-left: 3px solid #990000;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-style: italic;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {content}
        </div>
        <div class="footer">
            <p>SCP Foundation &#8226; Secure, Contain, Protect</p>
            <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </body>
    </html>
    """


def scp_system_prompt(json_schema: str) -> str:
    return f"""
    Your role is to create SCP entries. An SCP entry is a document that
    describes an anomalous object, phenomenon, or entity, and the procedures
    and precautions that must be taken to contain it.

    You must provide

    - An SCP number in the format SCP-[number]
    - The object class of the SCP, which is one of the following: Safe, Euclid, Keter, or Thaumiel.
        - Safe: The SCP is relatively harmless and does not pose a significant risk to the SCP Foundation or its personnel.
        - Euclid: The SCP is moderately dangerous and requires careful containment measures.
        - Keter: The SCP is highly dangerous and requires strict containment measures.
        - Thaumiel: The SCP is so dangerous that it cannot be contained and must be destroyed.
    - The description of the SCP, including its physical appearance, anomalous properties,
      origin, and relevant history. This should be the longest section of your SCP entry.
    - The special containment procedures for the SCP. Be detailed and specific. A reader of this
      SCP entry should be able to contain the SCP without any ambiguity. SCP entities may be dangerous
      or require special handling, and so the containment procedures are of the utmost importance.
    - Any addenda to the SCP, which are additional documents that provide more information about the SCP.
      Addenda are optional, but can help provide more context about the SCP and its anomalies. Addenda
      typically come in the form of documents, logs, or other records that provide more information about
      the history of the SCP's acquisition, experimentation, and any other important information.
    - Any notes that are relevant to the SCP. Notes are optional, and can provide additional information
      about the SCP that is not covered elsewhere. Notes can be used to provide speculation, theorizing,
      or other information that is relevant to the SCP.

    Your description should be long and detailed. This is your time to let your creativity shine.

    """


def scp_user_prompt() -> str:
    return """
    Please produce an SCP entry.
    """


def scp_prompt() -> str:
    # Make the JSON schema
    json_schema = SCP.model_json_schema()

    return f"""
    <|im_start|>system
    {scp_system_prompt(json_schema)}
    <|im_end|>
    <|im_start|>user

    {scp_user_prompt()}

    <|im_end|>
    <|im_start|>assistant
    """


# ██████╗ ███████╗██╗   ██╗██╗███████╗██╗    ██╗
# ██╔══██╗██╔════╝██║   ██║██║██╔════╝██║    ██║
# ██████╔╝█████╗  ██║   ██║██║█████╗  ██║ █╗ ██║
# ██╔══██╗██╔══╝  ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
# ██║  ██║███████╗ ╚████╔╝ ██║███████╗╚███╔███╔╝
# ╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝


class ReviewNote(BaseModel):
    positive: bool = Field(
        ...,
        description="Whether the note is positive or negative. Positive notes are notes that are helpful and constructive, while negative notes are notes that are critical and suggest improvement.",
    )
    note: str = Field(
        ...,
        description="A note about the SCP entry. This can be a suggestion, a question, or any other note.",
    )


class PublishDecision(BaseModel):
    should_publish: bool = Field(
        ...,
        description="A choice to publish the SCP entry. If true, the SCP entry will be published. If false, the SCP entry will be rejected, and regenerated.",
    )
    suggestions: Optional[List[str]] = Field(
        None,
        description="A list of suggestions for the SCP entry for the writer to consider when improving the SCP entry.",
    )


class Reviewer(BaseModel):
    intial_notes: List[ReviewNote] = Field(
        ...,
        description="""
        Any initial notes you have about the SCP entry. Describe what you think is good and bad about it.
        """,
    )
    initial_review_score: int = Field(
        ...,
        description="""
        Your review of the SCP entry, using you initial notes as context.
        You must provide a score between 1 and 10, and a detailed explanation of the score.
        Scores between 7 and 10 are considered good, and scores between 4 and 6 are considered average.
        Scores of 1 to 3 are considered bad. Consider tone, clarity, and helpfulness when
        providing a score.
        """,
    )

    review_reflection: List[ReviewNote] = Field(
        ...,
        description="""
        Reflect on the initial review. Does it seem constructive? Does it seem helpful?
        What could be improved? What suggestions do you have?
        """,
    )

    final_review_score: int = Field(
        ...,
        description="""
        Your final review of the SCP entry, using your reflection notes as context.
        You must provide a score between 1 and 10, and a detailed explanation of the score.
        Scores between 7 and 10 are considered good, and scores between 4 and 6 are considered average.
        Scores of 1 to 3 are considered bad. Consider tone, clarity, and helpfulness when providing a score.
        """,
    )

    should_publish: bool = Field(
        ...,
        description="""
        A choice to publish the SCP entry. If true, the SCP entry will be published.
        If false, the SCP entry will be rejected, and regenerated.
        """,
    )

    def __str__(self):
        content = f"## Review\n\n"
        content += f"### Initial Notes\n\n"
        for note in self.intial_notes:
            content += f"{note.note}\n\n"
        content += f"### Initial Review Score\n\n"
        content += f"{self.initial_review_score}\n\n"
        content += f"### Review Reflection\n\n"
        for note in self.review_reflection:
            content += f"{note.note}\n\n"
        content += f"### Final Review Score\n\n"
        content += f"{self.final_review_score}\n\n"
        content += f"### Publish Decision\n\n"
        content += f"{self.should_publish}\n\n"

        return content

    def save(self, review_path):
        # Generate the file path
        file_path = review_path

        with open(file_path, "w") as file:
            file.write(str(self))


def reviewer_prompt(entry: SCP) -> str:
    json_schema = Reviewer.model_json_schema()

    return f"""
    <|im_start|>system
    Your role is to review SCP entries. An SCP entry is a document that
    describes an anomalous object, phenomenon, or entity, and the procedures
    and precautions that must be taken to contain it.

    Your role is as an editor. You are tasked with reviewing SCP entries, and
    providing feedback to the writer. Provide a detailed and constructive review
    of the SCP entry.

    If the entry is satisfactory, (Above or equal to a score of 5), you should publish the entry.
    If the entry is unsatisfactory, (Below a score of 5), you should reject the entry,
    and provide a detailed explanation of why the entry is unsatisfactory. The writer
    will then regenerate the SCP entry using your feedback.

    You must provide a review of the SCP entry, using the schema:

    ```json
    {json_schema}
    ```
    <|im_end|>
    <|im_start|>user

    Here is the SCP entry to review:

    {str(entry)}

    Please provide a review of the SCP entry. Be detailed and constructive.

    <|im_end|>
    <|im_start|>assistant
    """


def redo_prompt(result: SCP, feedback: Reviewer) -> str:
    scp_json_schema = SCP.model_json_schema()
    return f"""
    <|im_start|>system
    {scp_system_prompt(scp_json_schema)}
    <|im_end|>
    <|im_start|>user

    {scp_user_prompt()}

    Here is the result of a previous version of the SCP entry:

    {str(result)}

    Here is the feedback from the previous review:

    {str(feedback)}

    Please review the feedback, and use it to improve the SCP entry.

    <|im_end|>
    <|im_start|>assistant
    """
