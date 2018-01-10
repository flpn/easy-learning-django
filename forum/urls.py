from django.urls import path

from . import views


app_name = 'forum'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='questions'),
    path('create/', views.QuestionCreateView.as_view(), name='create'),
    path('<str:slug>/', views.QuestionDetailView.as_view(), name='detail'),
    path('<str:slug>/update/', views.QuestionUpdateView.as_view(), name='update'),
    path('<str:slug>/delete/', views.QuestionDeleteView.as_view(), name='delete'),
    path('<str:slug>/like/', views.QuestionToggleLike.as_view(), name='toggle-like'),
    path('api/<str:slug>/like/', views.QuestionToggleLikeAPI.as_view(), name='toggle-like-api'),
]
