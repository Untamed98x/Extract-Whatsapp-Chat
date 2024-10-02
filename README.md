# WhatsApp Chat Cleaner

A Python script designed to automate the process of organizing and cleaning WhatsApp chat backups. This script searches for specific ZIP files containing WhatsApp chats, extracts their contents, renames the extracted text files, and organizes them into designated directories. It ensures that your WhatsApp chat backups are neatly arranged and easily accessible.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Script Overview](#script-overview)
- [Error Handling](#error-handling)
- [License](#license)
- [Contact](#contact)

## Features

- **Automatic Directory Detection**: Identifies the base directory where WhatsApp chat ZIP files are stored.
- **Pattern Matching**: Supports both Indonesian and English naming conventions for WhatsApp chat ZIP files.
- **Extraction & Renaming**: Extracts contents of ZIP files and renames text files for consistency.
- **Organized Storage**: Moves extracted and raw ZIP files into designated folders with timestamps.
- **Permission Checks**: Ensures the script has the necessary permissions to access and modify directories.
- **Error Handling**: Provides informative messages for any issues encountered during execution.

## Requirements

- **Python 3.6+**
- Standard Python libraries:
  - `os`
  - `zipfile`
  - `re`
  - `shutil`
  - `datetime`
  - `pathlib`

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/whatsapp-chat-cleaner.git
   cd whatsapp-chat-cleaner
   ```

2. **Ensure Python is Installed**

   Make sure you have Python 3.6 or higher installed. You can check your Python version with:

   ```bash
   python --version
   ```

3. **(Optional) Create a Virtual Environment**

   It's good practice to use a virtual environment to manage dependencies.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**

   No external dependencies are required as the script uses standard Python libraries.

## Usage

1. **Prepare Your Directories**

   - Ensure that your WhatsApp chat ZIP files are located in the following directory:

     ```
     /private/var/mobile/Library/Mobile Documents/com~apple~CloudDocs/
     ```

   - If the above path does not exist, the script will attempt to use the local Pyto Documents directory:

     ```
     Pyto/Documents/
     ```

   - Make sure the `SURCA/Function_Clean` directory exists in one of the above locations.

2. **Run the Script**

   Navigate to the directory containing the script and execute:

   ```bash
   python whatsapp_chat_cleaner.py
   ```

   Replace `whatsapp_chat_cleaner.py` with the actual filename if different.

3. **Script Execution**

   - The script will change the working directory to the base path.
   - It will search for ZIP files matching the patterns:
     - Indonesian: `Chat WhatsApp dengan*.zip`
     - English: `WhatsApp Chat with*.zip`
   - For each matching ZIP file:
     - Create a new directory with a timestamp.
     - Extract the contents of the ZIP file into the new directory.
     - Rename `.txt` files by removing specific prefixes.
     - Move the extracted folder to the `Extracted` directory.
   - Original ZIP files are moved to a `RAW_Extract` directory with a timestamp.
   - Optionally, old extracted folders matching specific patterns can be deleted.

4. **Output**

   After successful execution, you will find:

   - Extracted and renamed chat files in the `Extracted_WA_YYYYMMDD_HHMMSS` directory.
   - Raw ZIP files moved to the `RAW_Extract_WA_YYYYMMDD_HHMMSS` directory.

## Directory Structure

```
Function_Clean/
├── whatsapp_chat_cleaner.py
├── Extracted_WA_YYYYMMDD_HHMMSS/
│   ├── Chat1/
│   │   ├── Chat1.txt
│   │   └── ...
│   └── Chat2/
│       ├── Chat2.txt
│       └── ...
├── RAW_Extract_WA_YYYYMMDD_HHMMSS/
│   ├── Chat WhatsApp dengan XYZ.zip
│   └── WhatsApp Chat with ABC.zip
└── ...
```

## Script Overview

### 1. Importing Libraries

The script utilizes standard Python libraries for file operations, pattern matching, and date-time management.

### 2. Defining the Base Path

```python
base_path = Path("/private/var/mobile/Library/Mobile Documents/com~apple~CloudDocs/")
```

- Sets the primary directory where the script looks for WhatsApp chat ZIP files.
- If the primary path doesn't exist, it defaults to the local Pyto Documents directory.

### 3. Permission Checks

Ensures that the script has read and write permissions for the base directory.

### 4. Changing the Working Directory

```python
os.chdir(base_path)
```

Changes the current working directory to the base path for subsequent operations.

### 5. Pattern Matching for ZIP Files

Uses regular expressions to identify ZIP files following specific naming conventions in both Indonesian and English.

### 6. Extraction Process

- Creates a timestamped directory for extracted files.
- Extracts each matching ZIP file into a new folder.
- Renames `.txt` files by removing predefined prefixes.
- Moves the extracted folder to the `Extracted` directory.

### 7. Handling Raw ZIP Files

Creates a `RAW_Extract` directory and moves all original ZIP files into it.

### 8. Cleanup

Optionally deletes folders that match specific naming patterns to free up space.

## Error Handling

The script includes comprehensive error handling to manage issues such as:

- Missing directories
- Permission issues
- Corrupted ZIP files
- File renaming failures

Informative messages are printed to guide the user in resolving any encountered issues.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or suggestions, please contact [untamed98x@gmail.com](mailto:untamed98x@gmail.com).

---

*Happy Cleaning!*
