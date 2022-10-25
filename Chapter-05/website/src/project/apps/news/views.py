import datetime

# ============================================================================ #

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Article


class ArticleList(ListView):
    model = Article
    paginate_by = 10


def article_detail(request, slug):

    article = get_object_or_404(Article, slug=slug)

    today = datetime.date.today()
    version_1 = datetime.date.today() - datetime.timedelta(days=10)
    version_2 = datetime.date.today() - datetime.timedelta(days=30)
    version_3 = datetime.date.today() - datetime.timedelta(days=1)

    website = "https://www.youtube.com/watch?v=lLmFehmW_KQ"
    print("DATEEE", version_3)
    context = {
        "article": article,
        "today": today,
        "version_1": version_1,
        "version_2": version_2,
        "version_3": version_3,
        "website": website,
    }

    return render(request, "news/article_detail.html", context)
