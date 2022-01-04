from django.db import models

class Book(models.Model):
    #Release_Date = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='title')
    author = models.CharField(max_length=100, blank=True, default='author')
    language = models.CharField(max_length=20, blank=True, default='Language')
    text = models.TextField()

    class Meta:
        ordering = ['created']