from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('flashcards', views.flashcards, name='flashcards'),
]