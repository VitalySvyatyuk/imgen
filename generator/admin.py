from django.contrib import admin
from .models import GeneratedImage


@admin.register(GeneratedImage)
class GeneratedImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'width', 'height', 'size', 'format', 'color', 'created_at']
