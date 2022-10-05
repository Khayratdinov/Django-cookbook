from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from project.apps.core.admin import get_multilingual_field_names
from .models import Idea
from project.apps.core.admin import LanguageChoicesForm
from .models import Idea, IdeaTranslations

from project.apps.categories.models import Category


# @admin.register(Idea)
# class IdeaAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (_("Author and Category"), {
#             "fields": ["author", "categories"],
#         }),
#         (_("Title and Content"), {
#             "fields": get_multilingual_field_names("title") +
#             get_multilingual_field_names("content")
#         }),
#         (_("SEO"), {
#             "fields": ["meta_keywords", "meta_description", "meta_author", "meta_copyright"]
#         }),
#     ]
#     filter_horizontal = ["categories"]


class IdeaTranslationsForm(LanguageChoicesForm):
    class Meta:
        model = IdeaTranslations
        fields = "__all__"


class IdeaTranslationsInline(admin.StackedInline):
    form = IdeaTranslationsForm
    model = IdeaTranslations
    extra = 0


class IdeaForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        label=_("Categories"),
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
    )

    class Meta:
        model = Idea
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[
            "picture"
        ].widget.template_name = "core/widgets/image.html"


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    inlines = [IdeaTranslationsInline]
    fieldsets = [
        (_("Author and Category"),
         {"fields": ["author", "categories"]}),
        (_("Title and Content"),
            {"fields": ["title", "content", "picture"]}),
        (_("Ratings"),
            {"fields": ["rating"]}),
    ]
