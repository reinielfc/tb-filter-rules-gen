# Thunderbird Filter Rules Generator

This is a Python script to generate filter rules for the Thunderbird email client. It takes a YAML file containing filter rules and converts it into a .dat file that can be used by Thunderbird.

## Requirements

- Python 3.7 or later
- Jinja2
- Pydantic
- PyYAML

## Files

- `filter_gen.py`: The main script that reads the YAML configuration file and generates the `.dat` file.
- `model.py`: Defines the data models for the filter rules and implements the conversion to `.dat` file format.

## Usage

1. Install the required packages: \
   `pip install jinja2 pydantic pyyaml`
2. Create a YAML configuration file with your filter rules. See the example below for the format.
3. Run the script with the path to your YAML configuration file as an argument: \
   `python filter_gen.py <path_to_your_config_file.yaml>`\
    This will generate a `.dat` file in the same directory as the YAML file.

## Example YAML Configuration File

Here's an example of a YAML configuration file with a single filter rule:

```yml
home: "imap://johndoe%40gmail.com@imap.gmail.com"
main: "%5BExample%5D"
header:
  version: "9" # default
  logging: "no" # default
filters:
  - # NEWSLETTER
    name: newsletter
    enabled: "yes" # default
    type: "17" # default
    actions:
      - action: Mark flagged
      - action: Move to folder
        value: "{{home}}/{{main}}/Newsletters"
    condition:
      operator: OR # default
      criteria:
        - from,ends with,technewsletter.com
        - from,ends with,industryupdate.com
        - from,ends with,exampleinsights.com
        - from,is,updates@newsletter.example.com
```

OUTPUT:

```ini
version="9"
logging="no"
name="newsletter"
enabled="yes"
type="17"
action="Mark flagged"
action="Move to folder"
actionValue="imap://johndoe%40gmail.com@imap.gmail.com/%5BExample%5D/Newsletters"
condition="OR (from,ends with,exampleinsights.com) OR (from,ends with,industryupdate.com) OR (from,ends with,technewsletter.com) OR (from,is,updates@newsletter.example.com)"
```