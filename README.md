# Minecraft Recipe Converter (1.20.1 to 1.21+)

A lightweight Python script with a simple Graphical User Interface (GUI) to automatically update and migrate your Minecraft mod recipe JSON files from `1.20.x` to the new `1.21.1` or `1.21.2+` formats.

## ✨ Features

* **Folder Renaming:** Automatically renames the old `recipes` folder to the new `recipe` folder format required in 1.21+.
* **Result Tag Fix:** Converts the old `"item"` key inside the recipe result to the new `"id"` key.
* **Version-Specific Ingredient Handling:**
    * **1.21.1 Mode:** Keeps ingredients as objects (e.g., `{"item": "minecraft:wool"}`).
    * **1.21.2+ Mode:** Simplifies ingredients to direct strings (e.g., `"minecraft:wool"` or `"#minecraft:wool"` for tags) to match the newest Mojang standards.
* **Batch Processing:** Scans and updates all `.json` recipe files in the selected directory at once.

## 🚀 How to Use

1.  Make sure you have [Python](https://www.python.org/downloads/) installed on your system.
2.  Download the `converter.py` script.
3.  Run the script via your terminal or by double-clicking it:
    ```bash
    python converter.py
    ```
4.  A popup will appear asking which version you want to convert to:
    * Click **Yes** for `1.21.2+`
    * Click **No** for `1.21.1`
5.  Select your mod's data folder (e.g., the folder containing the `recipes` folder) in the file dialog.
6.  The script will process your files and show a success message with the number of updated recipes.

*Note: It is highly recommended to make a backup of your workspace before running any automated conversion scripts!*

## 💬 Support & Questions

If you run into any issues, have questions, or need help with modding, feel free to join the Discord server!

👉 **[Join our Discord Server](https://discord.gg/TUErNVMDHV)**
