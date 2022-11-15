from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
import os

# ============================================================================ #
from django.template.loader import render_to_string
from django.utils.timezone import now as timezone_now
from django.utils.text import slugify
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.forms import modelformset_factory
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import FileResponse, HttpResponseNotFound

# ============================================================================ #
from .forms import IdeaForm, IdeaTranslationsForm
from .models import Idea, IdeaTranslations
from .forms import IdeaFilterForm
from .models import Idea, RATING_CHOICES

# ============================================================================ #
PAGE_SIZE = getattr(settings, "PAGE_SIZE", 24)


@login_required
def download_idea_picture(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if idea.picture:
        filename, extension = os.path.splitext(idea.picture.file.name)
        extension = extension[1:]  # remove the dot
        response = FileResponse(idea.picture.file, content_type=f"image/{extension}")
        slug = slugify(idea.title)[:100]
        response["Content-Disposition"] = "attachment; filename=" f"{slug}.{extension}"
    else:
        response = HttpResponseNotFound(content="Picture unavailable")
    return response


# =============================== GENERATE PDF =============================== #


def idea_handout_pdf(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    context = {"idea": idea}
    html = render_to_string("ideas/idea_handout_pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = "inline; filename={date}-{name}-handout.pdf".format(
        date=timezone_now().strftime("%Y-%m-%d"), name=slugify(idea.translated_title)
    )

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)

    return response


# ================================= IDEA LIST ================================ #


def idea_list(request):
    qs = Idea.objects.order_by("title")
    form = IdeaFilterForm(data=request.GET)
    facets = {
        "selected": {},
        "categories": {
            "authors": form.fields["author"].queryset,
            "categories": form.fields["category"].queryset,
            "ratings": RATING_CHOICES,
        },
    }

    if form.is_valid():
        filters = (
            ("author", "author"),
            ("category", "categories"),
            ("rating", "rating"),
        )
        qs = filter_facets(facets, qs, form, filters)

    paginator = Paginator(qs, PAGE_SIZE)
    page_number = request.GET.get("page")
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:

        page = paginator.page(1)
    except EmptyPage:

        page = paginator.page(paginator.num_pages)

    context = {
        "form": form,
        "facets": facets,
        "object_list": page,
    }
    return render(request, "ideas/idea_list.html", context)


# =============================== FILTER FACETS ============================== #


def filter_facets(facets, qs, form, filters):
    for query_param, filter_param in filters:
        value = form.cleaned_data[query_param]
        if value:
            selected_value = value
            if query_param == "rating":
                rating = int(value)
                selected_value = (rating, dict(RATING_CHOICES)[rating])
            facets["selected"][query_param] = selected_value
            filter_args = {filter_param: value}
            qs = qs.filter(**filter_args).distinct()
    return qs


# ============================== IDEA LIST VIEW ============================== #
class IdeaListView(View):
    form_class = IdeaFilterForm
    template_name = "ideas/idea_list.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(data=request.GET)
        qs, facets = self.get_queryset_and_facets(form)
        page = self.get_page(request, qs)
        context = {"form": form, "facets": facets, "object_list": page}
        return render(request, self.template_name, context)

    def get_queryset_and_facets(self, form):
        qs = Idea.objects.order_by("title")
        facets = {
            "selected": {},
            "categories": {
                "authors": form.fields["author"].queryset,
                "categories": form.fields["category"].queryset,
                "ratings": RATING_CHOICES,
            },
        }

        if form.is_valid():
            filters = (
                ("author", "author"),
                ("category", "categories"),
                ("rating", "rating"),
            )
            qs = self.filter_facets(facets, qs, form, filters)
        return qs, facets

    @staticmethod
    def filter_facets(facets, qs, form, filters):
        for query_param, filter_param in filters:
            value = form.cleaned_data[query_param]
            if value:
                selected_value = value
                if query_param == "rating":
                    rating = int(value)
                    selected_value = (rating, dict(RATING_CHOICES)[rating])
                    facets["selected"][query_param] = selected_value
                    filter_args = {filter_param: value}
                    qs = qs.filter(**filter_args).distinct()
            return qs

    def get_page(self, request, qs):
        paginator = Paginator(qs, PAGE_SIZE)
        page_number = request.GET.get("page")
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return page


class IdeaList(ListView):
    model = Idea


class IdeaDetail(DetailView):
    model = Idea
    context_object_name = "idea"


def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    print("TESTTT", idea.picture.url)
    print("TESTTT 22", idea.picture_large.url)
    # print("TESTTT 33", idea.watermarked_picture_large.path)
    print("TESTTT 33", settings.STATIC_ROOT, "/site/img/watermark.png")

    context = {"idea": idea}

    return render(request, "ideas/idea_detail.html", context)


# =============================== CRUD FOR IDEA ============================== #


@login_required
def add_or_change_idea(request, pk=None):
    idea = None
    if pk:
        idea = get_object_or_404(Idea, pk=pk)
    IdeaTranslationsFormSet = modelformset_factory(
        IdeaTranslations, form=IdeaTranslationsForm, extra=0, can_delete=True
    )
    if request.method == "POST":
        print("STEP 1", request)
        form = IdeaForm(request, data=request.POST, files=request.FILES, instance=idea)
        translations_formset = IdeaTranslationsFormSet(
            queryset=IdeaTranslations.objects.filter(idea=idea),
            data=request.POST,
            files=request.FILES,
            prefix="translations",
            form_kwargs={"request": request},
        )
        if form.is_valid() and translations_formset.is_valid():
            idea = form.save()
            translations = translations_formset.save(commit=False)
            for translation in translations:
                translation.idea = idea
                translation.save()
            translations_formset.save_m2m()
            for translation in translations_formset.deleted_objects:
                translation.delete()
            return redirect("ideas:idea_detail", pk=idea.pk)
    else:
        print("STEP 2", request)
        form = IdeaForm(request, instance=idea)
        print("STEP 2", form)
        translations_formset = IdeaTranslationsFormSet(
            queryset=IdeaTranslations.objects.filter(idea=idea),
            prefix="translations",
            form_kwargs={"request": request},
        )

    context = {"idea": idea, "form": form, "translations_formset": translations_formset}
    return render(request, "ideas/idea_form.html", context)


@login_required
def delete_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    # if request.method == "POST":
    idea.delete()
    return redirect("ideas:idea_list")
    # context = {"idea": idea}
    # return render(request, "ideas/idea_deleting_confirmation.html", context)
