
from django.contrib import admin

from .models import Category, Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at')


admin.site.register(Category)
admin.site.register(Bookmark, BookmarkAdmin)
