# Abaqus Language Switcher

[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](https://github.com/LuckYang1/abaqus_language_switch/releases/tag/v1.0.0)
[![Abaqus](https://img.shields.io/badge/Abaqus-2016~2025-orange.svg)](https://www.3ds.com/products-services/simulia/products/abaqus/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 如需查看本文档的中文版本，请点击[这里](README.md)

## Introduction

This is a simple tool for switching the Abaqus interface language (Chinese/English) without modifying system regional settings, providing a quick and convenient solution.

## Download

You can obtain this tool in the following ways:

- **[Download the compiled executable](https://github.com/LuckYang1/abaqus_language_switch/releases/latest)** - Run directly without Python environment
- Or follow the instructions below to get the source code and run/compile it yourself

## Getting the Code

### Using Git Clone

If you have Git installed, you can clone the repository with the following commands:

```
git clone https://github.com/LuckYang1/abaqus_language_switch.git
cd abaqus_language_switch
```

### Direct Download

You can also download the code directly as a ZIP file from the [GitHub download page](https://github.com/LuckYang1/abaqus_language_switch/archive/refs/heads/main.zip).

## Running the Source Code Directly

1. Make sure you have Python 3.6 or higher installed on your system
2. Download the `abaqus_language_switch_exe.py` file to your local machine
3. Right-click on the file and select "Run as administrator" (or run it through the command line with administrator privileges)
   ```
   python abaqus_language_switch_exe.py
   ```
4. Follow the on-screen instructions to operate

Note: Running the Python script directly still requires administrator privileges because it needs to modify the configuration file in the Abaqus installation directory.

## About the Configuration Files

### locale.txt

This tool mainly modifies the Abaqus language configuration file `locale.txt`. This file is the original language configuration file for Abaqus, usually located at:

```
C:\SIMULIA\EstProducts\2021\win_b64\SMA\Configuration\locale.txt
```

The path may vary slightly depending on the Abaqus version. This file contains configuration information for the Abaqus interface language, mainly controlling the display language of the software (English, Chinese, or Japanese).

The tool achieves language switching by modifying the following settings in the configuration file:
- `[Alias]` section: Defines the mapping relationship between system locale settings and Abaqus language
- `[Default]` section: Sets whether to use the local language by default (`1 = yes`, `0 = no`)

The `locale_en.txt` file included in this project is a reference configuration file for English mode, which can be used to restore the English interface.

### abaqus_lang_settings.json

The tool creates and uses a settings file `abaqus_lang_settings.json` in the user's directory, located at:

```
C:\Users\your_username\AbaqusLangSwitcher\abaqus_lang_settings.json
```

This file stores the following information:
- `current_path`: The current Abaqus configuration file path being used
- `path_list`: All Abaqus installation paths added by the user, including path name, full path, and time added

The tool automatically updates this file when adding or switching Abaqus installation paths. If you have multiple Abaqus versions or installation locations, this feature allows you to easily switch between different configurations.

## Packaging as an Executable

### Prerequisites

1. Python 3.6 or higher installed on your computer
2. Internet connection (for installing packaging tools)

### Packaging Instructions

1. First, install the PyInstaller packaging tool:
   ```
   pip install pyinstaller
   ```

2. Open a command prompt (cmd) and navigate to the script directory:
   ```
   cd path_to_file
   ```

3. Execute the packaging command:
   
   Basic packaging command:
   ```
   pyinstaller --onefile --console abaqus_language_switch_exe.py
   ```
   
   Packaging command with custom icon:
   ```
   pyinstaller --onefile --console --icon=icon.ico abaqus_language_switch_exe.py
   ```
   If you want to use a custom icon, make sure there is an `icon.ico` file in the same directory as the script, or modify the icon path in the above command.

4. Wait for the packaging to complete, which may take a few minutes

5. After packaging is complete, you can find the generated exe file in the `dist` folder in the current directory
   (`dist/abaqus_language_switch_exe.exe`)

6. Copy the generated exe file to any location for use

## Usage Instructions

1. Since the program needs to modify system files, please right-click the exe file or Python script and select "Run as administrator"

2. When running for the first time, the program will automatically create a backup of the Abaqus configuration file

3. Follow the interface prompts to select the corresponding operation:
   - Option 1: Switch to Chinese mode
   - Option 2: Switch to English mode
   - Option 3: Restore initial backup
   - Option 4: Manage configuration file paths
   - Option 5: Exit program

## Notes

1. If your Abaqus installation path is different from the default path, you can add a new path through the "Manage configuration file paths" option in the program

2. The generated exe file can be run directly on Windows systems without installing Python or other dependencies

3. If you encounter errors such as "access denied", please make sure to run the program as an administrator

4. The backup file is saved in the same directory as the configuration file, with the filename `locale.txt.bak`

## Extending Support for Other Languages

Currently, the tool supports switching between Chinese and English. If you need to support other languages (such as Japanese), you can modify the `abaqus_language_switch_exe.py` file to implement this. The main points to modify are as follows:

1. Add a function like `switch_to_japanese()` based on the `switch_to_chinese()` function
2. Modify the corresponding regular expressions to find and update Japanese-related configuration lines
3. Add Japanese switching options to the main menu in the `print_menu()` function

For example, to add Japanese support, you can refer to the following code snippet:

```python
def switch_to_japanese():
    """Switch to Japanese mode"""
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: Configuration file not found: {CONFIG_PATH}")
        return
        
    try:
        # Read file content
        with open(CONFIG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Check if already in Japanese mode
        if 'Japanese_Japan.932 = ja_JP' in content and 'ja_JP = 1' in content:
            print("Already in Japanese mode!")
            return
            
        # Modify ja_JP default value
        content = re.sub(r'ja_JP = 0', 'ja_JP = 1', content)
            
        # Write back to file
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("Successfully switched to Japanese mode!")
        print("Please restart Abaqus to apply the changes.")
        
    except Exception as e:
        print(f"Error: Failed to switch to Japanese mode: {str(e)}")
        print(traceback.format_exc())
```

Refer to the configuration information in the `locale_en.txt` file to understand how each language is set up, allowing you to extend support for more languages.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 