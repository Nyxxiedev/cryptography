# cryptography

A Python tool for encrypting and decrypting files using symmetric encryption. Comes in two versions — a command-line version and a GUI version.

## About

This project uses the `cryptography` library's Fernet implementation to encrypt and decrypt files. A key is automatically generated and saved to disk on first run, then reused for all future operations.

## Requirements

- Python 3
- `cryptography` library
- `tkinter` (only needed for the GUI version — usually comes with Python)

## Installation

```bash
git clone https://github.com/CatLovinpersons/cryptography.git
cd cryptography
```

Then set up a virtual environment and install the dependency:

```bash
python3 -m venv venv
source venv/bin/activate
pip install cryptography
```

## Versions

### CLI (`cli-encrypt.py`)

Run it from the terminal:

```bash
python cli-encrypt.py
```

You'll be asked what you'd like to do:
```
what would you like to do?
1        # encrypt a file
2        # decrypt a file
```

Then enter the filename:
```
what file do you want to encrypt?
secret.txt
```

Files are modified in-place — the original content is replaced with the encrypted or decrypted version.

### GUI (`encrypt.py`)

Run it from the terminal:

```bash
python encrypt.py
```

A window will open with:
- A text field to enter the filename
- An **open** button to load and decrypt the file contents into the text box
- A **save** button to encrypt and save whatever is in the text box back to the file

## How the Key Works

On startup, both versions look for an existing `key.key` file. If none is found, a new Fernet key is generated and saved there automatically.

> **Important:** Keep your `key.key` file safe. If it's lost, any files encrypted with it cannot be recovered. The same key must be used to decrypt a file that was encrypted with it.