from django.urls import path
from . import views

urlpatterns = [
    path('getAllBooks/', views.RedirectionBooksList.as_view()),
    path('getAllIndex/', views.RedirectionIndexList.as_view()),
    path('getGraph/', views.RedirectionGraph.as_view()),
    path('Books/Search/<str:word>/', views.RedirectionSimpleSearch.as_view()),
]