# Beanconqueror to Obsidian - Export Beans as markdown files

## Pull requests welcomed

## Introduction

This project provides a Python script that converts your Beanconqueror JSON export into markdown files suitable for use with [Obsidian](https://obsidian.md/). The script reads a `config.yaml` file to determine which properties to include in the output.

## Features

- Convert Beanconqueror JSON data for beans into Obsidian-friendly markdown files.
- Adds metadata as frontmatter.
- Configurable options via `config.yaml` to control what data is included.
- Supports linking images stored in a specific folder.

## Requirements

- Python 3.6+
- `pyyaml` package

You can install the required Python package using pip:

```bash
pip install -r requirements.txt
```

## Usage 
Take a look at the at `config.yaml` turn off any properties you don't want to be outputted, run the script with

```bash
python script.py

```

## License
This project is free to use as you please