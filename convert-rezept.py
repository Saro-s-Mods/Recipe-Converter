import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def fix_recipe_content(data):
    """Passt den Inhalt eines Rezepts an die 1.21 Syntax an."""
    modified = False
    
    top_level_count = data.pop("count", None)

    if "result" in data:
        result = data["result"]
        
        if isinstance(result, str):
            data["result"] = {
                "id": result,
                "count": top_level_count if top_level_count is not None else 1
            }
            modified = True
            
        elif isinstance(result, dict):
            if "item" in result:
                result["id"] = result.pop("item")
                modified = True
            
            if top_level_count is not None and "count" not in result:
                result["count"] = top_level_count
                modified = True
                
    return data, modified

def run_fixer():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Wähle deinen Mod-ID Ordner (z.B. 'saros_road_blocks_mod')")
    
    if not folder_selected:
        return

    old_recipes_path = os.path.join(folder_selected, "recipes")
    new_recipe_path = os.path.join(folder_selected, "recipe")

    if os.path.exists(old_recipes_path):
        if os.path.exists(new_recipe_path):
            for file in os.listdir(old_recipes_path):
                shutil.move(os.path.join(old_recipes_path, file), os.path.join(new_recipe_path, file))
            os.rmdir(old_recipes_path)
        else:
            os.rename(old_recipes_path, new_recipe_path)
        print(f"Ordner umbenannt: {new_recipe_path}")
    
    target_path = new_recipe_path if os.path.exists(new_recipe_path) else folder_selected

    count_files = 0
    for root_dir, _, files in os.walk(target_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if "type" in data:
                        new_data, was_modified = fix_recipe_content(data)
                        if was_modified:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                json.dump(new_data, f, indent=2)
                            count_files += 1
                except Exception as e:
                    print(f"Fehler in {file}: {e}")

    messagebox.showinfo("Fertig!", f"Migration abgeschlossen!\n{count_files} Rezepte wurden aktualisiert und der Ordner wurde korrigiert.")

if __name__ == "__main__":
    run_fixer()
