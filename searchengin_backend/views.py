from django.db import models
from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse
from searchengin_backend.models import BookM, BookMIndex
from searchengin_backend.serializers import BookMIndexSerializer, BookMSerializer
from rest_framework.views import APIView
import json


# ----------------------------- Afficher tt les livres  

class RedirectionBooksList(APIView):
    def get(self, request, format=None):
        books = BookM.objects.all()
        jsondata = BookMSerializer(books, many=True)

        objectdata = {}
        objectdata['status'] = "200 OK"
        objectdata['message'] = "liste of books"
        objectdata['data'] = jsondata.data

        ## json.dumps() function converts a Python object into a json string.
        jsonString = json.dumps(objectdata)

        return HttpResponse(jsonString, content_type="application/json", status=200, reason="get all books in database")

# ----------------------------- Afficher tt les indexs 

class RedirectionIndexList(APIView):
    def get(self, request, format=None):
        indexs = BookMIndex.objects.all()
        jsondata = BookMIndexSerializer(indexs, many=True)

        objectdata = {}
        objectdata['data'] = jsondata.data
        jsonString = json.dumps(objectdata)

        return HttpResponse(jsonString, content_type="application/json", status=200, reason="get all indexes in database")


# ---------------------------- Recherche Simple par id unique 

# Affiche un livre avec son id ==> peut etre utils plus même n'est pas demandé
class RedirectionBookById(APIView):
    def get_object(self, idBook):
        try:
            return BookM.objects.get(id=idBook) ## renvoi l'objet avec id (dans la base) = id
        except BookM.DoesNotExist:
            raise Http404
    
    def get(self, request, id, format=None):
        book = self.get_object(id)

        print("------------------> book object : "+str(book))
        data = BookMSerializer(book)

        print("------------------> book object data : "+str(data))
        print("------------------> details data of book with id : "+str(id)+"\n -> "+str(data.data))
        return HttpResponse(str(data.data), content_type="application/json", status=200, reason="get one books by his id")

# ----------------------------- Recherche Simple Par Mot   

class RedirectionSimpleSearch(APIView):
    def get_object(self,word):
        try:
            return BookMIndex.objects.filter(attributes__words__icontains = word)  ## recherche par objet, pas par mot 
        except BookMIndex.DoesNotExist:
            raise Http404

    def get(self, request, word, format=None):
        indexs = self.get_object(word) ## renvoie un querySet

        print("--------> searched word : "+word)
        for e in indexs:
            print("------------------> index objects after filter : "+str(e.attributes))

        data = BookMIndexSerializer(indexs,many=True)
        return HttpResponse(json.dumps(data.data), content_type="application/json", status=200, reason="get indexs accepting filter condition") 

# --------------------------- Recherche Avancé : aho-ullman algo (projet 1) 

### T O D O

