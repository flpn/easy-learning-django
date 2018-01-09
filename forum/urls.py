from django.urls import path

from . import views


urlpatterns = [
    path('', views.QuestionListView.as_view(), name='questions'),
    path('<slug:slug>/', views.QuestionDetailView.as_view(), name='detail'),
]