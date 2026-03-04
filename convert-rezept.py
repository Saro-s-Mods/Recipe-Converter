import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def fix_ingredient(ing, target_version):
    if target_version == "1.21.2+":
        if isinstance(ing, dict):
            if "item" in ing: return ing["item"]
            if "tag" in ing: return "#" + ing["tag"]
    else:
        if isinstance(ing, str):
            if ing.startswith("#"): return {"tag": ing[1:]}
            else: return {"item": ing}
    return ing

def fix_recipe_content(data, target_version):
    modified = False
    top_level_count = data.pop("count", None)
    
    if "result" in data:
        result = data["result"]
        if isinstance(result, str):
            data["result"] = {"id": result, "count": top_level_count if top_level_count is not None else 1}
            modified = True
        elif isinstance(result, dict):
            if "item" in result:
                result["id"] = result.pop("item")
                modified = True
            if top_level_count is not None and "count" not in result:
                result["count"] = top_level_count
                modified = True

    if "key" in data and isinstance(data["key"], dict):
        for k, v in data["key"].items():
            old_val = data["key"][k]
            new_val = fix_ingredient(v, target_version)
            if old_val != new_val:
                data["key"][k] = new_val
                modified = True
                
    if "ingredients" in data and isinstance(data["ingredients"], list):
        for i in range(len(data["ingredients"])):
            if isinstance(data["ingredients"][i], list):
                for j in range(len(data["ingredients"][i])):
                    old_val = data["ingredients"][i][j]
                    new_val = fix_ingredient(data["ingredients"][i][j], target_version)
                    if old_val != new_val:
                        data["ingredients"][i][j] = new_val
                        modified = True
            else:
                old_val = data["ingredients"][i]
                new_val = fix_ingredient(data["ingredients"][i], target_version)
                if old_val != new_val:
                    data["ingredients"][i] = new_val
                    modified = True

    return data, modified

def run_fixer():
    root = tk.Tk()
    root.withdraw()
    
    is_1_21_2 = messagebox.askyesno("Select Version", "Convert to 1.21.2+?\n\n(Yes = 1.21.2+  |  No = 1.21.1)")
    target_version = "1.21.2+" if is_1_21_2 else "1.21.1"
    
    folder_selected = filedialog.askdirectory(title="Select your Mod-ID folder")
    if not folder_selected:
        return

    old_dir = os.path.join(folder_selected, "recipes")
    new_dir = os.path.join(folder_selected, "recipe")

    if os.path.exists(old_dir):
        if os.path.exists(new_dir):
            for file in os.listdir(old_dir):
                shutil.move(os.path.join(old_dir, file), os.path.join(new_dir, file))
            os.rmdir(old_dir)
        else:
            os.rename(old_dir, new_dir)
    
    target_path = new_dir if os.path.exists(new_dir) else folder_selected
    count_files = 0
    
    for root_dir, _, files in os.walk(target_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if "type" in data:
                        new_data, was_modified = fix_recipe_content(data, target_version)
                        if was_modified:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                json.dump(new_data, f, indent=2)
                            count_files += 1
                except Exception:
                    pass

    messagebox.showinfo("Done!", f"Migration to {target_version} complete!\n{count_files} files were updated.")

if __name__ == "__main__":
    run_fixer()
