# cryptography

A Python command-line tool for encrypting and decrypting files using symmetric encryption.

## About

This project uses the `cryptography` library's Fernet implementation to encrypt and decrypt files in-place. A key is automatically generated and saved to disk on first run, then reused for all future operations.

## How It Works

On startup, the program looks for an existing `key.key` file. If none is found, it generates a new Fernet key and saves it. It then prompts you to choose an action:

- `1` — Encrypt a file
- `2` — Decrypt a file

You provide the filename, and the file's contents are encrypted or decrypted in-place.

## Requirements

- Python 3
- `cryptography` library

## Installation

```bash
pip install cryptography
```

## Usage

```bash
python encrypt.py
```

You'll be asked what you'd like to do:
```
what would you like to do?
1        # encrypt a file
```
Then enter the filename:
```
what file do you want to encrypt?
secret.txt
```

> **Important:** Keep your `key.key` file safe. If it's lost, any files encrypted with it cannot be recovered.

## Notes

- Files are modified in-place — the original content is replaced with the encrypted/decrypted version.
- The same key must be used to decrypt a file that was encrypted with it.