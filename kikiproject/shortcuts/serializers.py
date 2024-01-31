from rest_framework import serializers
from shortcuts.models import ShortcutKey
        
class ShortcutKeySerializer(serializers.ModelSerializer):
    keys_list = serializers.SerializerMethodField()

    class Meta:
        model = ShortcutKey
        fields = ['category', 'description', 'platform', 'keys_list', 'index', 'bookmark']
        
    def get_keys_list(self, obj):
        return obj.keys.split(' ')