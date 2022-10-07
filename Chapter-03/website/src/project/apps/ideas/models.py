import uuid
import contextlib
import os

from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from django.utils.timezone import now as timezone_now

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from project.apps.core.model_fields import TranslatedField
from project.apps.core.models import (
    CreationModificationDateBase, UrlBase
)

RATING_CHOICES = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)


def upload_to(instance, filename):
    now = timezone_now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"ideas/{now:%Y/%m}/{instance.pk}{extension}"


class Idea(CreationModificationDateBase, UrlBase):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="authored_ideas",
    )
    title = models.CharField(_("Title"), max_length=200)
    content = models.TextField(_("Content"))

    categories = models.ManyToManyField(
        "categories.Category",
        verbose_name=_("Categories"),
        related_name="category_ideas",
    )
    rating = models.PositiveIntegerField(
        _("Rating"),
        choices=RATING_CHOICES,
        blank=True,
        null=True
    )
    translated_title = TranslatedField("title")
    translated_content = TranslatedField("content")

    picture = models.ImageField(
        _("Picture"), upload_to=upload_to
    )
    picture_social = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(1024, 512)],
        format="JPEG",
        options={"quality": 100},
    )
    picture_large = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(800, 400)],
        format="PNG"
    )
    picture_thumbnail = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(728, 250)],
        format="PNG"
    )

    class Meta:
        verbose_name = _("Idea")
        verbose_name_plural = _("Ideas")

    @property
    def structured_data(self):
        from django.utils.translation import get_language

        lang_code = get_language()
        data = {
            "@type": "CreativeWork",
            "name": self.translated_title,
            "description": self.translated_content,
            "inLanguage": lang_code,
        }
        if self.author:
            data["author"] = {
                "@type": "Person",
                "name": self.author.get_full_name() or self.author.username,
            }
        if self.picture:
            data["image"] = self.picture_social.url
        return data

    def delete(self, *args, **kwargs):
        from django.core.files.storage import default_storage
        if self.picture:
            with contextlib.suppress(FileNotFoundError):
                default_storage.delete(
                    self.picture_social.path
                )
                default_storage.delete(
                    self.picture_large.path
                )
                default_storage.delete(
                    self.picture_thumbnail.path
                )
            self.picture.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_url_path(self):
        return reverse("ideas:idea_detail", kwargs={"pk": self.pk})




class IdeaTranslations(models.Model):
    idea = models.ForeignKey(
        Idea,
        verbose_name=_("Idea"),
        on_delete=models.CASCADE,
        related_name="translations",
    )
    language = models.CharField(_("Language"), max_length=7)
    title = models.CharField(_("Title"), max_length=200)
    content = models.TextField(_("Content"))

    class Meta:
        verbose_name = _("Idea Translations")
        verbose_name_plural = _("Idea Translations")
        ordering = ["language"]
        unique_together = [["idea", "language"]]

    def __str__(self):
        return self.title
