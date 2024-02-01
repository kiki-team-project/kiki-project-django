from django.contrib import admin

from .models import (
    Post,
    Comment,
    PlatformList,
    CategoryList,
)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PlatformList)
admin.site.register(CategoryList)

