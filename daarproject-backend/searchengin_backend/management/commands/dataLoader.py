from django.core.management.base import BaseCommand, CommandError
from searchengin_backend.validator import AttributesSchema
from searchengin_backend.models import BookM, BookMIndex, JaccardGraph
from searchengin_backend.serializers import BookMSerializer
import requests
import html2text

from searchengin_backend.utils import getWordList, printBook, printErrorMessage, printSuccesMessage, serializeIndex, numberWordOfString

class Command(BaseCommand):
    
    help = 'Load data from api'

    # netoyer la base 
    def clearDatabase(self):
        BookM.objects.all().delete()
        BookMIndex.objects.all().delete()
        JaccardGraph.objects.all().delete()

    # renvoyer le nombre de mots dans une chaine
    def numberWordOfString(text : str):
        word_list = text.split()
        return len(word_list)

    # fonction principal handler 
    def handle(self, *args, **options) :
        bookMap = {}
        sizeDB : int = 150
        minNumberWords : int = 1000
        page_num : int = 0
        counter = 0
        numberBooksStocked : int = 0
        api_url = "https://gutendex.com/"

        self.clearDatabase()

        while (numberBooksStocked < sizeDB):
            page_num += 1
            self.stdout.write(self.style.SUCCESS('-------- page web id : '+str(page_num)+' --------'))
            
            # recupérer tt les livres
            response = requests.get(api_url+'/books?mime_type=text&'+'page='+str(page_num))
            jsondata = response.json()
            books = jsondata['results']

            for book in books: 
                    textBook : str = ""
                    if (numberBooksStocked > sizeDB):
                        break

                    # >> contruire la table des livres 
                    idBook = book['id']
                    title = book['title']
                    author = ('unknown' if len(book['authors']) == 0 else book['authors'][0]['name'])
                    lang = book['languages'][0]
                    if (lang != "fr" and lang != "en"):
                        continue
                    try:
                        cover = book['formats']['image/jpeg'] # 26272
                    except:
                        cover ='unknown' 
                    try:
                        url_book = book['formats']["text/plain; charset=utf-8"]
                        url_book = url_book.replace(".zip", ".txt")
                        book_html = requests.get(url_book).text
                        h = html2text.HTML2Text()
                        h.ignore_links = True
                        textBook = h.handle(book_html)
                        numberWords : int = numberWordOfString(textBook)
                    except:
                        continue
                    
                    if (numberWords >= minNumberWords):
                        counter  = counter + 1
                        numberBooksStocked += 1
                        printBook(self,idBook,counter)
                        serializer = BookMSerializer(data = { "id":idBook, "title":title, "author":author, "lang":lang, "body":url_book, "cover":cover })

                        if serializer.is_valid(raise_exception=True):
                            serializer.save() 
                            printSuccesMessage(self,' >> sucess adding book : '+str(idBook))

                            # contruire la table d'indexage 
                            text_response = title+" ".join(book['subjects'])
                            words = getWordList(text_response,lang)
                            indexbject = {'idIndex': counter, 'idBook' : idBook, 'words': words,
                            }
                            bookMap[idBook] = words
                            AttributesSchema(**indexbject)
                            serializeIndex(self,indexbject,counter)
                        else:
                            printErrorMessage(self,' >> error adding book with id : "%s"'% id)