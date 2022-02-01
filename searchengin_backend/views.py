from ast import Str
from operator import index
from tkinter.tix import Tree
from django.db import models
from django.http.response import Http404
from django.http import HttpResponse
from searchengin_backend.models import BookM, BookMIndex, JaccardGraph
from searchengin_backend.serializers import BookMIndexSerializer, BookMSerializer, JaccardGraphSerializer
import json
import math 
from collections import Counter
from rest_framework.views import APIView
import sys
import subprocess

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

# ----------------------------- Afficher tt le graph de suggestions (livres et leurs voisins)
class RedirectionGraph(APIView):
    def get(self, request, format=None):
        graph = JaccardGraph.objects.all()
        jsondata = JaccardGraphSerializer(graph, many=True)
        objectdata = {}
        objectdata['data'] = jsondata.data
        jsonString = json.dumps(objectdata)
        return HttpResponse(jsonString, content_type="application/json", status=200, reason="get graph")

# ----------------------------- Recherche Simple Par Mot  + Suggestions
class RedirectionSimpleSearch(APIView):
    #Retourne vraie si l'expression reguliere est reduite à une suite de concatenations
    def estSuiteConcatenations(self, regEx : str):
        for i in range(len(regEx)):
            if (((regEx[i] == '*') | (regEx[i] == '|')) | (regEx[i] == '.')):
                return False
        return True

    def run_regEx_command(self, command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return iter(p.stdout.readline, b'')

    def result_command(self, word:str, regEx:Str):
            for output_line in self.run_regEx_command(['java', '-jar', 'regExSearch.jar', regEx, word]):
                if(len(output_line)>0):
                    return '#'
            return ''

    def containsRegEx(self, book, regEx:Str):
            listWords = book.attributes['words']
            united_text_words = '\n'.join(listWords)
            if (self.result_command(united_text_words, regEx)):
                    return True
            return False

    def get_object(self,word):
        try:
            if (self.estSuiteConcatenations(word)):
                return BookMIndex.objects.filter(attributes__words__icontains = word)
            else:
                listBookIndex = []
                for book in BookMIndex.objects.all():
                    if (self.containsRegEx(book, word)):
                        listBookIndex.append(book) 
                return listBookIndex
        except BookMIndex.DoesNotExist:
            raise Http404

    def getWordsCounter(self, id):
        index = BookMIndex.objects.filter(attributes__idBook=id)
        for e in index:
            wordsCount = e.attributes['words']
        return Counter(wordsCount)

    def updateBooksRank(self):
        # centrality = (number of nodes - 1) / sum(distance from node to all other nodes)
        print("\n")
        graph = JaccardGraph.objects.all()
        for booknode in graph:
            print("idBook = "+str(booknode.bookId)+" ---> distanceTotal = "+str(booknode.totalDistance)) 
            nodeslen = JaccardGraph.objects.count() 
            centrality = nodeslen / booknode.totalDistance
            book = BookM.objects.get(id=booknode.bookId)
            book.rank = centrality
            book.save()


    def get(self, request, word, format=None):
        print(" ------------------------------------------------------- search begin -----------------------------------------------------")
        
        bookMap, bookMapIdWords, objectdata = ({} for i in range(3))
        originbooks, suggestions =  ([] for i in range(2))
        jaccardDistance = 80 
        result = self.get_object(word)
        books = []
        for e in result:
            bookid          = e.attributes['idBook']
            wordslist       = e.attributes['words']
            wordsmap = Counter(wordslist)
            bookMap[bookid] = wordsmap[word] 
            bookMapIdWords[bookid] = wordsmap ## cette map contient que les occ des livre resultats, pas celle dans le graphe
            originbooks.append(bookid)
            books += BookM.objects.filter(id=bookid) 

        bookMap2 = dict(sorted(bookMap.items(), key=lambda item: item[1],reverse=True))
        mostPertinentBooks = list(bookMap2)[:3]

        for bookPertinentId in mostPertinentBooks:  ## les 3 livres pertinents de chaque recherche 
            neighbors = list(removekey(bookMap,bookPertinentId)) 
            words_occ_pertinent = bookMapIdWords[bookPertinentId]
            print("\n")
            exist = JaccardGraph.objects.filter(bookId=bookPertinentId).exists()
            if exist:
                book = JaccardGraph.objects.get(bookId=bookPertinentId)
            for neighborId in list(neighbors):
                words_occ_neighbor = bookMapIdWords[neighborId]
                distance = calculJaccardDistance(words_occ_pertinent , words_occ_neighbor)
                if math.floor(distance*100) > jaccardDistance or (exist==True and neighborId in book.neighbors):
                    neighbors.remove(neighborId)

            # vérifier si le livre déja dans le graphe + mettre à jour ses voisins 
            if exist == True: 
                updatedNeighbors = book.neighbors + neighbors             
                book.neighbors = list(set(updatedNeighbors))
                suggestions += book.neighbors                            
                book.save()
            else :
                graph = JaccardGraph.objects.all()
                distPertinent = 0
                for g in graph:
                    word_occ_g    = self.getWordsCounter(g.bookId) 
                    dist =  calculJaccardDistance(words_occ_pertinent , word_occ_g)
                    printDistance(bookPertinentId, g.bookId, dist)
                    g.totalDistance += dist
                    distPertinent += dist
                    g.save()

                # ajouter ce nouveau noeud avec un distance total des autres noeuds
                serializerGraph = JaccardGraphSerializer( data = {
                        "bookId"    : bookPertinentId,
                        "neighbors" : neighbors,
                        "totalDistance" : distPertinent
                    }
                )
                saveGraph(serializerGraph)

            ## ajouter une arret inverse de chaque voisin
            for n in neighbors:
                if n not in mostPertinentBooks:
                    if JaccardGraph.objects.filter(bookId=n).exists():
                        b = JaccardGraph.objects.get(bookId=n)
                        updatedN = b.neighbors + [bookPertinentId]
                        b.neighbors = list(set(updatedN))
                        b.save()
                    else:
                        graph = JaccardGraph.objects.all()
                        distN = 0
                        for g in graph:
                            word_occ_g    = self.getWordsCounter(g.bookId) 
                            dist2 =  calculJaccardDistance(bookMapIdWords[neighborId] , word_occ_g) 
                            printDistance(n, g.bookId, dist2)
                            g.totalDistance += dist2
                            distN += dist2
                            g.save()
                        
                        serializerGraph2 = JaccardGraphSerializer( data = {
                            "bookId"    : n,
                            "neighbors" : [bookPertinentId],
                            "totalDistance" : distN
                           }
                        )
                        saveGraph(serializerGraph2)
                
        ## -------------------------- classement : closeness algorithm / our graph is already set - update book rank
        self.updateBooksRank()

        ## ------------------- resume
        suggestions = list(dict.fromkeys(suggestions))
        suggestions = [id for id in suggestions if id not in originbooks]

        suggbooks = []
        for sid in suggestions[:5]:
            suggbooks += BookM.objects.filter(id=sid) 
            
        print("\nsearched word  -> "+str(word))
        print("top three        -> "+str(mostPertinentBooks))
        print("original res     -> "+str(originbooks))
        print("suggestion res   -> "+str(suggestions))

        # objectdata = {}
        objectdata['books']       = BookMSerializer(books, many=True).data
        objectdata['suggestions'] = BookMSerializer(suggbooks, many=True).data
        print(" ------------------------------------------------------- search end -------------------------------------------------------")
        return HttpResponse(json.dumps(objectdata), content_type="application/json", status=200, reason="get indexs accepting filter condition") 