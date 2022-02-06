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
import subprocess
import urllib.request
import string
import random
import itertools 
import time
from django.db.models import Max

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

# ----------------------------- Rechercher un livre dans la base de donneee par son id
class RedirectionBookById(APIView):
    def get(self, request, id, format=None):
        try:
            with urllib.request.urlopen("https://gutenberg.org/files/"+id +"/"+
                                id+"-h/"+id+"-h.htm") as url:
                textBook = url.read().decode('utf-8')
                return HttpResponse(textBook, content_type='text/html', status=200)
        except:
            pass

# ----------------------------- Afficher tt le graph de suggestions (livres et leurs voisins)
class RedirectionGraph(APIView):
    def get(self, request, format=None):
        graph = JaccardGraph.objects.all()
        jsondata = JaccardGraphSerializer(graph, many=True)
        objectdata = {}
        objectdata['data'] = jsondata.data
        jsonString = json.dumps(objectdata)
        return HttpResponse(jsonString, content_type="application/json", status=200, reason="get graph")

# ----------------------------- Recherche Simple Par Mot + Suggestions
class RedirectionSimpleSearch(APIView):
    #Retourne vraie si l'expression reguliere est reduite à une suite de concatenations
    def estSuiteConcatenations(self, regEx : str):
        for i in range(len(regEx)):
            if (((regEx[i] == '*') | (regEx[i] == '|')) | (regEx[i] == '.')):
                return False
        return True

    # Execute la commande passee en parametre pour requeter le fichier jar
    def run_regEx_command(self, command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return iter(p.stdout.readline, b'')

    # formule la command a effectuer sur le fichier jar pour rechercher la regEx dans le texte
    def result_command(self, text:str, regEx:Str):
            cpt = 0
            for _ in self.run_regEx_command(['java', '-jar', '../regExSearch.jar', regEx, text]):
                cpt += 1
            return cpt

    # Verifie si le livre contient des chaines de caracteres qui satisfant la regEx recherchee
    def containsRegEx(self, book, regEx:Str):
            listWords = book.attributes['words']
            united_text_words = '\n'.join(listWords)
            return (self.result_command(united_text_words, regEx))

    def random_hash(self, size=32, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    # Methode principale pour rechercher une regEx ou une chaine de caractere dans la base de donnee
    def get_object(self,word):
        try:
            if (self.estSuiteConcatenations(word)):
                listBookIndex = []
                for book in BookMIndex.objects.all():
                    words_book = book.attributes['words']
                    for w in words_book:
                        if str.lower(w) == str.lower(word):
                            listBookIndex.append(book)
                            break
                return listBookIndex
            else:
                listBookIndex = []
                newHash = str(self.random_hash())
                for book in BookMIndex.objects.all():
                    cpt = self.containsRegEx(book, word)
                    if (cpt>0):
                        listBookIndex.append(book)
                        l = book.attributes['words']
                        for i in range(cpt):
                            l.append(newHash)  
                        book.words = l
                        book.save()
                word = newHash
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
            nodeslen = JaccardGraph.objects.count() ## 15/distanceTotal
            if (booknode.totalDistance == 0):
                centrality = 0
            else:
                centrality = nodeslen / booknode.totalDistance
            book = BookM.objects.get(id=booknode.bookId)
            book.rank = centrality
            book.save()

    def callGarbageCollector(self):
        print("graph size : ",str(JaccardGraph.objects.count()))
        graph = JaccardGraph.objects.order_by("centrality") ## 39 - 25 = 14
        x = JaccardGraph.objects.count() - 25 
        i = 0
        for booknode in graph:
            if i<x : # 14
                i += 1
                print("==> remove object : ",str(booknode.centrality))
                JaccardGraph.objects.filter(bookId=booknode.bookId).delete()
            else:
                continue

    # Methode permettant de faire la recherche
    def get(self, request, word, format=None):
        print("===========____search begin____===========")

        JaccardGraph.objects.all().delete()
        start_time = time.time()
        bookMap, bookMapIdWords, objectdata = ({} for i in range(3))
        originbooks, suggestions =  ([] for i in range(2))
        jaccardDistance = 75
        l_books_matchs = self.get_object(word) ## 100 //

        books = [] 

        # >>> d = {320: 1, 321: 0, 322: 3}
        # >>> min(d, key=d.get)
        # 321
        for book_matchs in l_books_matchs: # pour chaque object de 20 
            bookId          = book_matchs.attributes['idBook']
            wordsList       = book_matchs.attributes['words']
            wordsmap = Counter(wordsList)
            
            if(len(books) < 10):
                bookMap[bookId] = wordsmap[word] 
                bookMapIdWords[bookId] = wordsmap
                originbooks.append(bookId) 
                books += BookM.objects.filter(id=bookId)  
            else:
                bookMap[bookId] = wordsmap[word] 
                min_key = min(bookMap, key=bookMap.get) ## récuperer le min valeur parmi la liste bookMap
                if bookMap[min_key] > bookMap[bookId]:  
                    continue
                else:
                    del bookMap[min_key]
                    del bookMapIdWords[min_key]
                    originbooks.remove(min_key)
                    books.remove(BookM.objects.get(id=min_key))
                    
                    bookMap[bookId] = wordsmap[word] 
                    bookMapIdWords[bookId] = wordsmap
                    originbooks.append(bookId) 
                    books += BookM.objects.filter(id=bookId)

        print("book len : ",len(books))
        print("bookMap len : ",len(bookMap))
        
        # selectionne les 3 livres ayant le plus d'occurences de la chaine de caractere recherchee 
        mostPertinentBooks = list(dict(sorted(bookMap.items(), key=lambda item: item[1],reverse=True)))[:3]

        for bookPertinentId in mostPertinentBooks:  
            neighbors = list(removekey(bookMap,bookPertinentId)) 
            words_occ_pertinent = bookMapIdWords[bookPertinentId]
            print("\n")
            # exist nous indique si le livre est deja sauvegarder dans le graph de jaccard
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
                nodeslen = JaccardGraph.objects.count() 
                if (distPertinent == 0):
                    centrality = 0
                else:
                    centrality = nodeslen / distPertinent
                serializerGraph = JaccardGraphSerializer( data = {
                        "bookId"    : bookPertinentId,
                        "neighbors" : neighbors,
                        "totalDistance" : distPertinent,
                        "centrality" : centrality
                    }
                )
                saveGraph(serializerGraph)
                book = BookM.objects.get(id=bookPertinentId)
                book.rank = centrality
                book.save()


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
                        
                        nodeslen = JaccardGraph.objects.count() 
                        if (distN == 0):
                            centrality = 0
                        else:
                            centrality = nodeslen / distN
                        serializerGraph2 = JaccardGraphSerializer( data = {
                            "bookId"    : n,
                            "neighbors" : [bookPertinentId],
                            "totalDistance" : distN,
                            "centrality" : centrality
                           }
                        )
                        saveGraph(serializerGraph2)
                        
                        # modifier le rang du livre correspondant au livre dans le graphe (pour les voisins)
                        book = BookM.objects.get(id=n)
                        book.rank = centrality
                        book.save()
                

        # Social , Modern, Fiction, Women 
        if JaccardGraph.objects.count() >= 35: 
            self.callGarbageCollector()


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
        
        print("--- %s seconds ---" % (time.time() - start_time))
        print("===========____search begin ends____===========",)
        return HttpResponse(json.dumps(objectdata), content_type="application/json", status=200, reason="get indexs accepting filter condition") 