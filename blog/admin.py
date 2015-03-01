from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from blog.models import Post, Comment, Tag
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField

class PostAdmin(MarkdownModelAdmin):
    list_display = ("title", "created_on")
    prepopulated_fields = {"slug": ("title",)}
    # Next line is a workaround for Python 2.x
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)

