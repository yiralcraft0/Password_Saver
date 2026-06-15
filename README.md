# 🔒 Password Manager

**Author:** Priyanshu (*YiralcrafT*)

This is my first GitHub repository 😁. I was thinking about what project I should upload first, and then I remembered the Password Manager project I built in Python a few weeks ago.

## About the Project

I created this Password Manager project to improve my Python programming skills and gain hands-on experience with real-world applications. Through this project, I explored file handling, encryption techniques, password security concepts, and various Python modules.

While this project was primarily created for learning purposes, it demonstrates my understanding of Python fundamentals, modular programming, and basic cybersecurity concepts.

**A secure password manager built with Python.**

## Features

* 🔐 Password encryption
* 🔑 PIN authentication
* 📁 JSON-based storage
* ➕ Add passwords
* 👀 View passwords
* ✏️ Rename entries
* 🗑️ Delete entries
* 📋 Copy passwords to clipboard

## Requirements

### Required Modules

```python
from cryptography.fernet import Fernet
import bcrypt
import json
import os
import subprocess
import sys
```

### Clipboard Support

```python
import pyperclip
```

### Styling & Interactive Experience

```python
from colorama import Fore, Style, init
import time
```

## Note

This project was created for educational purposes and to improve my understanding of Python, encryption, and secure data handling.
