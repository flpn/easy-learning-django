from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Question


class QuestionListView(ListView):
    model = Question


class QuestionDetailView(DetailView):
    def get_object(self, *args, **kwargs):
        question = Question.objects.get(slug=self.kwargs['slug'])
        question.increment_visualization()
        
        return question
