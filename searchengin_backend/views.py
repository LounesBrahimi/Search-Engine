from django.db import models
from django.http.response import Http404
from django.http import HttpResponse
from searchengin_backend.models import BookM, BookMIndex, JaccardGraph
from searchengin_backend.serializers import BookMIndexSerializer, BookMSerializer, JaccardGraphSerializer
from rest_framework.views import APIView
import json
import math 
from collections import Counter

from searchengin_backend.utils import calculJaccardDistance, removekey, saveGraph,printDistance

# ----------------------------- Afficher tt les livres  

class RedirectionBooksList(APIView):
    def get(self, request, format=None):
        books = BookM.objects.all()
        jsondata = BookMSerializer(books, many=True)

        objectdata = {}
        objectdata['status'] = "200 OK"
        objectdata['message'] = "list of books"
        objectdata['data'] = jsondata.data
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

class RedirectionBookById(APIView):
    def get_object(self, idBook):
        try:
            return BookM.objects.get(id=idBook)
        except BookM.DoesNotExist:
            raise Http404
    
    def get(self, request, id, format=None):
        book = self.get_object(id)
        data = BookMSerializer(book)
        return HttpResponse(str(data.data), content_type="application/json", status=200, reason="get one books by his id")

# ----------------------------- Recherche Simple Par Mot  + Suggestions

class RedirectionSimpleSearch(APIView):
    def get_object(self,word):
        try:
            return BookMIndex.objects.filter(attributes__words__icontains = word)
        except BookMIndex.DoesNotExist:
            raise Http404

    def getn(self):
        return 4

    def get(self, request, word, format=None):
        # JaccardGraph.objects.all().delete()
        bookMap = {}
        bookMapIdWords = {}
        objectdata = {}
        originbooks = []
        suggestions = []
        jaccardDistance = 60 ## %

        result = self.get_object(word) ##
        for e in result:
            bookid          = e.attributes['idBook']
            wordslist       = e.attributes['words']
            wordsmap = Counter(wordslist)
            bookMap[bookid] = wordsmap[word] 
            bookMapIdWords[bookid] = wordsmap
            originbooks.append(bookid)

        bookMap2 = dict(sorted(bookMap.items(), key=lambda item: item[1],reverse=True))
        mostPertinentBooks = list(bookMap2)[:3]


        for bookPertinentId in mostPertinentBooks: 
                # liste des voisins des 3 livres pertinents issue de la recherche 
                neighbors = list(removekey(bookMap,bookPertinentId))  ## neighbors = bookMap - bookPertinent
                
                # Map<word,occ> pour chaque livre pertinent
                words_occ_pertinent = Counter(bookMapIdWords[bookPertinentId])

                # conserver que les voisins qui respectent la distance de jaccard
                for neighborId in list(neighbors):
                    words_occ_neighbor  = Counter(bookMapIdWords[neighborId])
                    dist = calculJaccardDistance(words_occ_pertinent , words_occ_neighbor)*100  
                    printDistance(bookPertinentId, neighborId, dist)
                    if math.floor(dist) > jaccardDistance: 
                        neighbors.remove(neighborId)
                      
                # vérifier si le livre déja dans le graphe     
                exist = JaccardGraph.objects.filter(bookId=bookPertinentId).exists()
                if exist == True: 
                    print("------------------------------------- book "+str(bookPertinentId)+" already present in graph, add new node with new neighbors -------------------------------------")
                    
                    book = JaccardGraph.objects.get(bookId=bookPertinentId)
                    print("### book already in graph, update node neighbors")
                    updatedNeighbors = book.neighbors + neighbors
                    book.neighbors = list(set(updatedNeighbors))
                    suggestions += book.neighbors
                    book.save()
                    continue
                else :
                    print("------------------------------------- book "+str(bookPertinentId)+" is not present in graph, add new node with new neighbors -------------------------------------")
                   
                    serializerGraph = JaccardGraphSerializer( data = {
                            "bookId"    : bookPertinentId,
                            "neighbors" : neighbors
                        }
                    )
                    saveGraph(serializerGraph)
                    
        suggestions = list(dict.fromkeys(suggestions))
        suggestions = [id for id in suggestions if id not in originbooks]
        print("searched word  -> "+str(word))
        print("top three      -> "+str(mostPertinentBooks))
        print("original res   -> "+str(originbooks))
        print("suggestion res -> "+str(suggestions))

        objectdata['books']      = BookMIndexSerializer(result, many=True).data
        objectdata['suggestion'] = list(suggestions)[:5]

        return HttpResponse(json.dumps(objectdata), content_type="application/json", status=200, reason="get indexs accepting filter condition") 

# ----------------------------- Afficher tt le graph de suggestions (livres et leurs voisins)

class RedirectionGraph(APIView):
    def get(self, request, format=None):

        graph = JaccardGraph.objects.all()
        jsondata = JaccardGraphSerializer(graph, many=True)

        objectdata = {}
        objectdata['data'] = jsondata.data
        jsonString = json.dumps(objectdata)

        return HttpResponse(jsonString, content_type="application/json", status=200, reason="get graph")
