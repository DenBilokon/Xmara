from django.contrib import admin

from .models import Picture, Document, Video


@admin.register(Picture)
class Picture(admin.ModelAdmin):
    list_display = ["user_id", "title", "description", "image", "created_at"]
    list_filter = ["title"]
    ordering = ("title",)
    search_fields = ["title"]


@admin.register(Document)
class Document(admin.ModelAdmin):
    list_display = ["title", "document", "created_at"]
    list_filter = ["title"]
    ordering = ("title",)
    search_fields = ["title"]


@admin.register(Video)
class Video(admin.ModelAdmin):
    list_display = ["title", "video", "created_at"]
    list_filter = ["title"]
    ordering = ("title",)
    search_fields = ["title"]
