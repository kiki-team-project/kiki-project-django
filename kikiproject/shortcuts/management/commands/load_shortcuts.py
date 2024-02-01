import os
import json
from django.core.management import BaseCommand
from shortcuts.models import ShortcutKey, ProgramList
import base64
from PIL import Image
import io

class Command(BaseCommand):
    help = 'Load shortcuts data from a JSON file'

    def handle(self, *args, **kwargs):
        
        json_file_path = os.path.join(os.path.dirname(__file__), 'programlist.json')

        try:
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            platforms_data = data.get("platforms", [])
            
            for platform in platforms_data:               
                # 이미지 파일을 열기
                image_dir = f"shortcuts/management/commands/logo/{platform}.png"
                
                with open(image_dir, "rb") as image_file:
                    # 이미지를 읽고 Base64로 인코딩
                    encoded_string = base64.b64encode(image_file.read()).decode()
                
                ProgramList.objects.create(
                    platform=platform,
                    image = encoded_string
                )

            self.stdout.write(self.style.SUCCESS('Successfully loaded Community data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to load Community data: {str(e)}'))
        
        
        json_file_path = os.path.join(os.path.dirname(__file__), 'figma_shortcut.json')
        self.save_database(json_file_path, 'figma')
        
        json_file_path = os.path.join(os.path.dirname(__file__), 'excel_shortcut.json')
        self.save_database(json_file_path, 'excel')                         
            
    def save_database(self, json_file_path, platform):

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
                    platform = platform,
                    bookmark = 0,
                    index = i
                )

            self.stdout.write(self.style.SUCCESS('Successfully loaded shortcuts data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to load shortcuts data: {str(e)}'))
        
        
