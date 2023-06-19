from django.contrib import admin

from .models import Picture, Document, Video, Audio, Archive


@admin.register(Picture)
class Picture(admin.ModelAdmin):
    list_display = ["user_id", "title", "image", "created_at"]
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


@admin.register(Audio)
class Audio(admin.ModelAdmin):
    list_display = ["artist", "title", "audio", "created_at"]
    list_filter = ["title", "artist"]
    ordering = ("title", "artist")
    search_fields = ["title", "artist"]


@admin.register(Archive)
class Archive(admin.ModelAdmin):
    list_display = ["title", "archive", "created_at"]
    list_filter = ["title"]
    ordering = ("title",)
    search_fields = ["title"]
