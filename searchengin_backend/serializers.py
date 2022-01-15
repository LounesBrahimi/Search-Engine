from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from searchengin_backend.models import BookM, BookMIndex, JaccardGraph


class BookMSerializer(ModelSerializer):
    class Meta:
        model = BookM
        fields = ('id', 'title', 'author' , 'lang' , 'body', 'rank')

class BookMIndexSerializer(ModelSerializer):
    class Meta:
        model = BookMIndex
        fields = ('attributes',)
        # try:
        #     errors = model.validate(data['attributes'])
        # except Exception as errors:
        #     raise serializers.ValidationError(errors)
        # try:
        #     model(signup_ts='broken', friends=[1, 2, 'not number'])
        # except ValidationError as e:
        #     print(e.json())


class BookMIndexSerializer(ModelSerializer):
    class Meta:
        model = BookMIndex
        fields = ('attributes',)

class JaccardGraphSerializer(ModelSerializer):
    class Meta:
        model = JaccardGraph
        fields = ('id','bookId','neighbors',)