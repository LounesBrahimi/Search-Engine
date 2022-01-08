from django.urls import path
from . import views

urlpatterns = [
    path('gelAllBooks/', views.RedirectionBooksList.as_view()),
    path('gelAllIndex/', views.RedirectionIndexList.as_view()),
    path('Books/Search/<int:id>/', views.RedirectionBookById.as_view()),
    path('Index/Search/<str:word>/', views.RedirectionSimpleSearch.as_view()),
]