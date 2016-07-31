from django.contrib import admin
from .models import Post, Author, Category, Tag

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_date', 'author']
    list_display_links = ['updated_date']
    list_editable = ['title']
    list_filter = ['updated_date', 'author']
    search_fields = ['title', 'body']
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)

