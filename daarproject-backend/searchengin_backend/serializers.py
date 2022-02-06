from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from searchengin_backend.models import BookM, BookMIndex, JaccardGraph


class BookMSerializer(ModelSerializer):
    class Meta:
        model = BookM
        fields = ('id', 'title', 'author' , 'lang' , 'body', 'cover', 'rank')

class BookMIndexSerializer(ModelSerializer):
    class Meta:
        model = BookMIndex
        fields = ('attributes',)

class BookMIndexSerializer(ModelSerializer):
    class Meta:
        model = BookMIndex
        fields = ('attributes',)

class JaccardGraphSerializer(ModelSerializer):
    class Meta:
        model = JaccardGraph
        fields = ('id','bookId','neighbors','totalDistance','centrality')