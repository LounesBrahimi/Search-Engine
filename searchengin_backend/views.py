from django.db import models
from django.http.response import Http404
from django.http import HttpResponse
from searchengin_backend.models import BookM, BookMIndex, JaccardGraph
from searchengin_backend.serializers import BookMIndexSerializer, BookMSerializer, JaccardGraphSerializer
from rest_framework.views import APIView
import json
from collections import Counter

from searchengin_backend.utils import calculJaccardDistance, removekey, saveGraph

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

    def get(self, request, word, format=None):
        #JaccardGraph.objects.all().delete()
        bookMap = {}
        objectdata = {}
        originbooks = []
        suggestions = []
        jaccardDistance = 50

        result = self.get_object(word) 
        for e in result:
            bookid          = e.attributes['idBook']
            wordslist       = e.attributes['words']
            wordsmap = Counter(wordslist)
            bookMap[bookid] = wordsmap[word] 
            originbooks.append(bookid)

        bookMap2 = dict(sorted(bookMap.items(), key=lambda item: item[1],reverse=True))
        mostPertinentBooks = list(bookMap2)[:3]

        for bookPertinentId in mostPertinentBooks:
                neighbors = list(removekey(bookMap,bookPertinentId)) 
                exist = JaccardGraph.objects.filter(bookId=bookPertinentId).exists()
                if exist == True: 
                    book = JaccardGraph.objects.get(bookId=bookPertinentId)
                    print("### book already in graph, update node neighbors")
                    book.neighbors = list(set(book.neighbors+neighbors)) 
                    suggestions += book.neighbors
                    book.save()
                    continue
                else :
                    print("### book is not present in graph, add new node with new neighbors")

                    # verifier la distance de jaccard entre le bookPertinent et chacun de ses possible voisins
                    #print("------------>>>> "+str(neighbors))
                    for neighorId in neighbors:
                        #print("-----------> "+str(neighorId))
                        dist = calculJaccardDistance(bookPertinentId,neighorId) 
                        # if dist < jaccardDistance:
                        #     print("add this neighbour")
                        # else:
                        #     print('not add this neighbour')

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

        graphs = JaccardGraph.objects.all()
        jsondata = JaccardGraphSerializer(graphs, many=True)

        objectdata = {}
        objectdata['data'] = jsondata.data
        jsonString = json.dumps(objectdata)

        return HttpResponse(jsonString, content_type="application/json", status=200, reason="get graph")
