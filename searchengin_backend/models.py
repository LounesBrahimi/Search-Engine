from django.db import models
from typing import List


# Table des Livres : 
class BookM(models.Model):
    id     = models.IntegerField(primary_key=True)
    title  = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default="unknown")
    lang   = models.CharField(max_length=10)
    body   = models.TextField(default="this is our book body")     

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id','title'], name='unique')
        ]
        ordering = ['id' , 'title']


# Table d'indexage :
class BookMIndex(models.Model):
    attributes = models.JSONField(default=dict)


# Table represente le graphe de jaccard
class JaccardGraph(models.Model):
    id        = models.AutoField(primary_key=True)
    bookId    = models.IntegerField(default='-1') 
    neighbors = models.JSONField(default=dict,null=True) 


# class BookMIndexM(models.Model):
#     idIndex   = models.IntegerField(primary_key=True)
#     word      = models.CharField()
#     bookInfo  = models.JSONField(default=dict)

