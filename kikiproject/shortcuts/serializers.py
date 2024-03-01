from rest_framework import serializers
from shortcuts.models import ShortcutKey, ProgramList

class ProgramListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProgramList
        fields = ['id', 'platform', 'image_url', 'bookmark']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        else:
            return None
        
    
class ShortcutKeySerializer(serializers.ModelSerializer):
    keys_list = serializers.SerializerMethodField()

    class Meta:
        model = ShortcutKey
        fields = ['id', 'category', 'description', 'platform', 'keys_list', 'index', 'bookmark', 'image']
        
    def get_keys_list(self, obj):
        return obj.keys.split(' ')