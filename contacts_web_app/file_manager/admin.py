from django.contrib import admin

from .models import Library


@admin.register(Library)
class Library(admin.ModelAdmin):
    list_display = ["title", "description", "image"]
    list_filter = ["title"]
    ordering = ("title",)
    search_fields = ["title"]
