import os
import json

def handle():
    json_file_path = os.path.join(os.path.dirname(__file__), 'shortcuts.json')
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        shortcuts_data = data.get("shortcuts", [])
        for shortcut_data in shortcuts_data:
            category = shortcut_data.get("category", "")
            keys = shortcut_data.get("keys", [])
            description = shortcut_data.get("description", "")
            print("keys : "," ".join(keys))
            print("category : ",category)
            print("description : ",description)
    except Exception as e:
        print(e)
        
handle()