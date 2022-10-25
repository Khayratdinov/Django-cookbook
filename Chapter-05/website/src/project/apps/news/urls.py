from django.urls import path

from .views import ArticleList, article_detail


urlpatterns = [
    path("", ArticleList.as_view(), name="article_list"),
    path("<slug:slug>/", article_detail, name="article_detail"),
]
