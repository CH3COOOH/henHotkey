# henHotkey

A simple hotkey manager written in Python.  
This tool lets you define custom keyboard shortcuts in a JSON file to either run commands or paste strings.

---

## Features
- **Lightweight and easy to use**: define hotkeys with a simple JSON configuration.  
- **No installation required**: just clone the repo and run with Python.  
- **Supports both string paste and command execution** 
- **Configuration file included**: see `template.json` for reference.

---

## Installation
Clone the repository:

```bash
git clone https://github.com/CH3COOOH/henHotkey.git
cd henHotkey
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage
Run the program with a configuration file:

```bash
python main.py <template.json>
```

Replace `<template.json>` with your own configuration file.  
You can use the provided `template.json` as a starting point.

---

## Configuration
Hotkeys are defined in a JSON file. Each entry maps a key combination to an action.

### Action types
- **`str::`** → Paste a string  
  Example: `"ctrl+alt+1": "str::なんで春日影やったの！？😡"`  
  *(You can omit `str::` since string mode is the default.)*
- **`run::`** → Execute a system command  
  Example: `"ctrl+alt+3": "run::cmd /c start cmd /k"`

### Example (`template.json`)
```json
{
  "ctrl+alt+1": "なんで春日影やったの！？😡",
  "ctrl+alt+2": "私にできることならなんでもするから……！😭",
  "ctrl+alt+3": "run::cmd /c start cmd /k",
  "ctrl+alt+4": "str::run::cmd /c start cmd /k"
}
```

---

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

