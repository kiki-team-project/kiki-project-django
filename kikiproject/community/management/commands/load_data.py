import os
import json
from django.core.management import BaseCommand
from community.models import PlatformList, CategoryList 

class Command(BaseCommand):
    help = 'Load shortcuts data from a JSON file'

    def handle(self, *args, **kwargs):
        json_file_path = os.path.join(os.path.dirname(__file__), 'basedata.json')

        try:
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            categorys_data = data.get("categorys", [])
            platforms_data = data.get("platforms", [])
            
            for category in categorys_data:
                CategoryList.objects.create(
                    category=category,
                )
            
            for platform in platforms_data:
                PlatformList.objects.create(
                    platform=platform,
                )

            self.stdout.write(self.style.SUCCESS('Successfully loaded Community data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to load Community data: {str(e)}'))