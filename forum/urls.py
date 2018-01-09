from django.urls import path

from . import views


app_name = 'forum'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='questions'),
    path('<slug:slug>/', views.QuestionDetailView.as_view(), name='detail'),
    path('<str:slug>/like/', views.like, name='like'),
    path('<str:slug>/dislike/', views.dislike, name='dislike'),
]
