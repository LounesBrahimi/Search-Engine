from rest_framework import serializers
from searchengin_backend.models import BookM

class BookSerializer(serializers):
    class Meta:
        model = BookM
        fields = ('id', 'title', 'author', 'body' , 'lang')