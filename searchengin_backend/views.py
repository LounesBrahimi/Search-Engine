from django.shortcuts import render
from django.http import HttpResponse
from searchengin_backend.models import BookM
from searchengin_backend.serializers import BookSerializer
# from rest_framework.response import Response
from rest_framework.views import APIView
import json

class RedirectionBooksList(APIView):
    def get(self, request, format=None):
        books = BookM.objects.all()
        jsondata = BookSerializer(books, many=True)

        objectdata = {}
        objectdata['status'] = "200 OK"
        objectdata['message'] = "liste of books"
        objectdata['data'] = jsondata.data

        ## json.dumps() function converts a Python object into a json string.
        jsonString = json.dumps(objectdata)

        return HttpResponse(jsonString, content_type="application/json", status=200, reason="get all books in database")


# class RedirectionListeDeProduits(APIView):
#     def get(self, request, format=None):
#         response = requests.get(baseUrl+'products/')
#         jsondata = response.json()
#         return Response(jsondata)


# #    def post(self, request, format=None):
# #        NO DEFITION of post --> server will return "405 NOT ALLOWED"
