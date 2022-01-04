from django.urls import path
from . import views

urlpatterns = [
    path('', views.RedirectionBooksList.as_view()),
]