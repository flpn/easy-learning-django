from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, RedirectView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


class QuestionListView(ListView):
    def get_queryset(self):
        query = self.request.GET.get('query')
        ordering = self.request.GET.get('ordering')

        if query:
            queryset = Question.objects.all().search(query)
        else:
            queryset = Question.objects.all()

        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset


class QuestionDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['form'] = AnswerForm
        
        return context

    def get_object(self, *args, **kwargs):
        question = Question.objects.get(slug=self.kwargs['slug'])
        question.increment_visualization()

        return question


class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'forum/question_create.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user

        return super(QuestionCreateView, self).form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'forum/question_update.html'
    form_class = QuestionForm
    model = Question
    

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('forum:questions')


class QuestionToggleLike(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        question = get_object_or_404(Question, slug=slug)
        url_ = question.get_absolute_url()
        user = self.request.user

        if user.is_authenticated():
            if user in question.likes.all():
                question.likes.remove(user)
            else:
                question.likes.add(user)

        return url_


class QuestionToggleLikeAPI(LoginRequiredMixin, APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        question = get_object_or_404(Question, slug=slug)
        url_ = question.get_absolute_url()
        user = self.request.user
        updated = liked = False

        if user.is_authenticated:
            if user in question.likes.all():
                question.likes.remove(user)
            else:
                liked = True
                question.likes.add(user)
            
            updated = True
        
        data = {'updated': updated, 'liked': liked}

        return Response(data)


class AnswerCreate(LoginRequiredMixin, CreateView):
    template_name = 'forum/question_detail.html'
    form_class = AnswerForm

    def form_valid(self, form):
        slug = self.request.POST.get('slug')

        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.question = get_object_or_404(Question, slug=slug)

        # Refactor this.
        instance.question.views -= 1
        instance.question.save()

        return super(AnswerCreate, self).form_valid(form)
