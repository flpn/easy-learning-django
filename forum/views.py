from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Question


class QuestionListView(ListView):
    model = Question


class QuestionDetailView(DetailView):
    def get_object(self, *args, **kwargs):
        return Question.objects.get(slug=self.kwargs['slug'])
