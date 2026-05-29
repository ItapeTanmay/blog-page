from django.contrib import admin
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','category','created_at']
    prepopulated_fields = {'slug':('title',)}

















