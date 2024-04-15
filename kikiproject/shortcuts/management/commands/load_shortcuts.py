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
                # ImageModel 인스턴스 생성
                instance = ProgramList(platform=platform)
                
                # 이미지 파일 업로드 (예시 파일 경로: 'path/to/image.jpg')
                image_path = f'/images/{platform}.svg'
                instance.image = image_path  
                instance.bookmark = 0             
                # 데이터베이스에 저장
                instance.save()             
                

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
                
                image_path = f'/images/{platform}.svg'
             
                ShortcutKey.objects.create(
                    category=category,
                    keys=keys,
                    description=description,
                    platform = platform,
                    bookmark = 0,
                    index = i,
                    image = image_path
                )

            self.stdout.write(self.style.SUCCESS('Successfully loaded shortcuts data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to load shortcuts data: {str(e)}'))
        
        
