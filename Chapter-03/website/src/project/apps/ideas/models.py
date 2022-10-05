import uuid
 
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
 
  class Meta:
    verbose_name = _("Idea") 
    verbose_name_plural = _("Ideas")
 
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