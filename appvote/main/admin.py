from django.contrib import admin
from .models import category, discussion

@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
@admin.register(discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at')
    list_filter = ('category', 'author')
    search_fields = ('title', 'content')
    
    def author(self, obj):
        return obj.author.username if obj.author else obj.author2
    author.short_description = 'Author'
