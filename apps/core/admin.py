from django.contrib import admin
from .models import DemoItem

@admin.register(DemoItem)
class DemoItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
