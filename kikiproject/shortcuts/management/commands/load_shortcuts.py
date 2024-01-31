import os
import json
from django.core.management import BaseCommand
from shortcuts.models import ShortcutKey 

class Command(BaseCommand):
    help = 'Load shortcuts data from a JSON file'

    def handle(self, *args, **kwargs):
        json_file_path = os.path.join(os.path.dirname(__file__), 'shortcuts.json')

        try:
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            shortcuts_data = data.get("shortcuts", [])
            for i, shortcut_data in enumerate(shortcuts_data):
                category = shortcut_data.get("category", "")
                keys = shortcut_data.get("keys", [])
                keys = " ".join(keys)
                description = shortcut_data.get("description", "")

                ShortcutKey.objects.create(
                    category=category,
                    keys=keys,
                    description=description,
                    platform = "figma",
                    bookmark = 0,
                    index = i
                )

            self.stdout.write(self.style.SUCCESS('Successfully loaded shortcuts data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to load shortcuts data: {str(e)}'))
