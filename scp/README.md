# SCP entry generator

## Overview
This Python script generates SCP (Secure, Contain, Protect) entries and saves them to the `entries` directory. The script uses the `outlines` library for generating the SCP entries based on a predefined schema.

Special thanks to [all the contributors](https://scp-wiki.wikidot.com/authors-pages) of the SCP wiki over the years! This would never be possible without the creativity, passion, and dedication of the SCP community.

## Features
- Supports various SCP object classes: Safe, Euclid, Keter, Thaumiel, and more can be added as needed.
- Generates SCP entries with the following sections:
  - Item Number
  - Object Class
  - Special Containment Procedures
  - Description
  - Addenda (optional)
  - Notes (optional)
- Saves the generated SCP entries as text files in the `entries` directory.

## Dependencies
- `pydantic`: A data validation and settings management library.
- `typing`: Standard library module for type annotations.
- `enum`: Standard library module for creating enumeration types.
- `json`: Standard library module for working with JSON data.
- `outlines`: A library for generating text based on a provided schema.
- `os`: Standard library module for interacting with the operating system.

## Usage
1. Ensure you have the necessary dependencies installed:
  ```
  pip install -r requirements.txt
  ```

2. Run the script to generate a new SCP entry.
  ```
  python scp.py
  ```

3. The generated entry will be saved in the `entries` directory with the file name `SCP-{id}.txt`.

## Example
```python
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
```

This will generate a new SCP entry, save it to the `entries` directory, and print the file path.

## Customization
You can customize the script by:

- Adding new `ObjectClass` values as needed.
- Modifying the `ContainmentProcedures`, `Description`, `Addendum`, and `Note` models to fit your desired SCP entry structure.
- Adjusting the text generation and formatting in the `save()` method of the `SCP` model.

## Contributing
If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.
