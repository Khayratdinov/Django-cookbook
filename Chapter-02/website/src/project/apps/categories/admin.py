from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from project.apps.core.admin import get_multilingual_field_names

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Title"), {"fields": get_multilingual_field_names("title")})
    ]