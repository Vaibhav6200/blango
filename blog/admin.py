from django.contrib import admin
from blog.models import *

# Register your models here.
class PostAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}
  list_display = ['title', 'slug' ,'published_at']

admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)