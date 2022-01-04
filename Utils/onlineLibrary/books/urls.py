from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from books import views

urlpatterns = [
    path('books/', views.book_list),
    path('books/<int:pk>/', views.book_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)