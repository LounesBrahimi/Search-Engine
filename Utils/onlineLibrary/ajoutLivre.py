from books.models import Book
from books.serializers import BookSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

book = Book(title='Un premier Livre')
book.save()