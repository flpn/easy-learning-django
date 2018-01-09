from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Question


class QuestionListView(ListView):
    model = Question


class QuestionDetailView(DetailView):
    def get_object(self, *args, **kwargs):
        print(self.request)

        question = Question.objects.get(slug=self.kwargs['slug'])
        question.increment_visualization()

        return question


def like(request, slug):
    question = get_object_or_404(Question, slug=slug)
    question.like()

    return HttpResponseRedirect(reverse('forum:detail', args=(question.slug,)))



def dislike(request, slug):
    question = get_object_or_404(Question, slug=slug)
    question.dislike()

    return HttpResponseRedirect(reverse('forum:detail', args=(question.slug,)))
