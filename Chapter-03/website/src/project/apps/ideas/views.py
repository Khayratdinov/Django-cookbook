from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .forms import IdeaForm
from .models import Idea


class IdeaList(ListView):
    model = Idea


class IdeaDetail(DetailView):
    model = Idea
    context_object_name = "idea"


@login_required
def add_or_change_idea(request, pk=None):
    idea = None
    if pk:
        idea = get_object_or_404(Idea, pk=pk)

    if request.method == "POST":
        form = IdeaForm(
            data=request.POST,
            files=request.FILES,
            instance=idea
        )

        if form.is_valid():
            idea = form.save()
            return redirect("ideas:idea_detail", pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)

    context = {"idea": idea, "form": form}
    return render(request, "ideas/idea_form.html", context)


@login_required
def delete_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == "POST":
        idea.delete()
        return redirect("ideas:idea_list")
    context = {"idea": idea}
    return render(request, "ideas/idea_deleting_confirmation.html", context)
