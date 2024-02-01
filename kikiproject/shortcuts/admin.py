from django.contrib import admin

from .models import (
    ShortcutKey,
    ProgramList
)

admin.site.register(ShortcutKey)
admin.site.register(ProgramList)