from rest_framework.serializers import ModelSerializer
from searchengin_backend.models import BookM

class BookSerializer(ModelSerializer):
    class Meta:
        model = BookM
        fields = ('id', 'title', 'author' , 'lang' , 'body')

        ## python manage.py makemigrations
        ## python manage.py migrate  
        ## python manage.py dataLoader 1 2 ==> [1 2]
        ## python manage.py runserver