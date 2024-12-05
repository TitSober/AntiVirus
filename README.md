# AntiVirus
*YARA based antivirus built in python

# YARA Scripts Overview

This directory contains several scripts designed to handle YARA rules, which are used for pattern matching within files and data streams. The scripts are part of a YARA-based antivirus solution written in Python. Below is an in-depth explanation of each script and its components.

## YaraLoader.py

### Class: YaraLoader

- **Purpose**: Loads YARA rules from files and parses them into usable objects.
- **Key Fields**:
  - `rule_path`: The file path where YARA rules are stored.

- **Key Methods**:
  - `__init__(self, rule_path)`: Initializes the YaraLoader with a specified path to YARA rule files.
  - `load_rules(self)`: Walks through the directory specified by `rule_path`, reads YARA files, and parses them into rule objects using `_parse_rules`.
  - `_parse_rules(self, rule_text)`: Uses `YaraParser` to parse the rule text into rule objects.

## YaraParser.py

### Class: YaraParser

- **Purpose**: Parses the text of YARA rules into structured data components.
- **Key Fields**:
  - `rules`: A list to store parsed rule objects.

- **Key Methods**:
  - `__init__(self, rule_text)`: Initializes the parser with rule text and initiates parsing.
  - `split2(self, string, delim)`: Splits a string by a delimiter and cleans the result.
  - `parse_rules(self, rule_text)`: Splits rule text into components and parses each using helper methods.
  - `parse_meta(self, rule_body)`: Extracts metadata from rule text.
  - `parse_strings(self, rule_body)`: Extracts strings used in matching from rule text.
  - `parse_condition(self, rule_body, strings)`: Extracts and processes the condition under which the rule triggers.
  - `get_rules(self)`: Returns the list of parsed rules.

## YaraRule.py

### Class: YaraRule

- **Purpose**: Represents a single YARA rule with its components.
- **Key Fields**:
  - `name`: The name of the rule.
  - `meta`: Metadata associated with the rule.
  - `strings`: Strings used in the rule's condition.
  - `condition`: The condition that must be met for the rule to trigger.

- **Key Methods**:
  - `__init__(self, name, meta, strings, condition)`: Initializes a new YaraRule with its components.
  - `print_rule(self)`: Outputs the rule's components to the console.
  - `getName(self)`: Returns the rule's name.
  - `getMeta(self)`: Returns the rule's metadata.
  - `getStrings(self)`: Returns the rule's strings.
  - `getCondition(self)`: Returns the rule's condition.

## YaraCompiler.py

### Class: YaraCompiler

- **Purpose**: Compiles and processes YARA conditions into executable forms.
- **Key Methods**:
  - `__init__(self)`: Initializes the YaraCompiler.
  - `tokenize(self, condition_string)`: Breaks a condition string into tokens for processing.
  - `shunting_yard(self, condition_string)`: Converts a condition string using the shunting yard algorithm into a format for evaluation.
  - `precedence(self, operator)`: Determines the precedence of operators for condition processing.

These scripts collectively allow for the loading, parsing, representation, and compilation of YARA rules, enabling the detection of patterns within files and data streams as part of an antivirus solution.
