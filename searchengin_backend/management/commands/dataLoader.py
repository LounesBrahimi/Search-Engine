from django.core.management.base import BaseCommand, CommandError
from searchengin_backend.models import BookM
from searchengin_backend.serializers import BookSerializer
import requests
import re
from collections import Counter

## pour declarer une commande, : il suffit de définir une classe Command comme sous-classe de BaseCommand 
## il suffit de lancer la commande : python manage.py dataLoader <arg>.
class Command(BaseCommand):

    ## declarations
    help = 'Load data from api'

    ## peut etre on a besoin de cette méthode pour ajouter un argument
    def add_arguments(self, parser): 
        parser.add_argument('page_id', nargs='+', type=int)

    ## fonction handler 
    def handle(self, *args, **options) :

        # delete oldest books
        BookM.objects.all().delete()
        ## declaration
        api_url = "https://gutendex.com/"
        myurl = "http://127.0.0.1:8000/"
        pages_web_num = 4 
        nbBook = 1664 ## nombre de livre min dans la biblio
        nbWords = 10000 ## chaque livre doit avoir au min 10 000 mots

        ## recuperer le parametre
        p_num = options['page_id']
        self.stdout.write('numero de page web : "%s"' % p_num)

        ## pour avoir 1664 il faut parcourir 52 page web
        # while(pages_web_num*32 % nbBook != 0) :
        #         pages_web_num = pages_web_num + 1
    
        ## boucle principale : 
        # for i in range(1,3)
        counter = 0
        for i in p_num: ## dans chaque page web on recupere 32 books => 2*32 = 64
            
            self.stdout.write(self.style.SUCCESS('-------- page web id : '+str(i)+' --------'))

            response = requests.get(api_url+'/books?mime_type=text&'+'page='+str(i))
            jsondata = response.json()
            books = jsondata['results']

            for book in books: ## pour chaque livre
                # words = re.findall('[a-zA-Z\u00C0-\u00FF]*', body) ## body : url vers le texte
                # if len(words) < 10000:
                #     continue
                # else : 
                    counter  = counter + 1
                    id = book['id']
                    title = book['title']
                    author = ('unknown' if len(book['authors']) == 0 else book['authors'][0]['name'])
                    lang = book['languages'][0]
                    try:
                        body = book['formats']["text/plain; charset=utf-8"]
                        body = body.replace(".zip", ".txt")
                    except:
                        continue
                    
                    # print json content
                    self.stdout.write(self.style.SUCCESS(' ---- begin ---- '))
                    self.stdout.write('book '+str(counter)+' / book id : "%s"' % id)
                    self.stdout.write('title : "%s"' % title)
                    #self.stdout.write('book author : "%s"' % author)
                    #self.stdout.write('book lang : "%s"' % lang)
                    #self.stdout.write('book text : "%s"' % body)
                    #self.stdout.write(self.style.SUCCESS(' ---- end ---- '))

                    serializer = BookSerializer(data={
                            "id":id,
                            "title":title,
                            "author":author,
                            "lang":lang,
                            "body": body
                        }
                    )

                    if serializer.is_valid(raise_exception=True):
                        serializer.save() # we can call .save() to return an object instance, based on the validated data. method save() will create a new instance.
                        ##self.stdout.write(self.style.SUCCESS(' ---> sucess adding book with id : "%s"'% id))

                        text_response = (book['title']) + "  ".join(book['subjects'])
                        # self.stdout.write(' --------->   '+text_response)
                        # c = Counter(['eggs', 'ham', 'eggs', 'sess'])
                        # self.stdout.write(' val ---------> '+str(c)) ## Counter({'eggs': 2, 'ham': 1, 'sess': 1})
                        
                    else:
                        self.stdout.write(self.style.ERROR(' ---> error adding book with id : "%s"'% id))


                ## blabla 
                ## index (
                #     idindex    : 1
                #     List<Mots> : "aa"
                #     idBook     :  1
                # )

                ## recherche simple : 
                #


                ## reche regex
                ## utiliser la biblio regex

                

                ## code pour faire l'indexation : 
                        # algo(texte) : 
                        #    recuperer tt les mots du texte
                        #    supprimer les mots non utils / stop words
                        #    calculer l'occurence de chaque mots
                        #    stocker le resultat dans une matrice/map... word/occ
                        #    implementer un autre algo qui renvoie une liste d'object : [{word,bookid}] ==> [{word="aa",id="23"} 
                        #                                                                                     , {word="bb",id=23}]
                        #    appeler le serialize pour stocker l'indexage


                ## code pour calculer le graphe de jackard --> il va nous servir pour faire la partie de suggestion
                ## List<Books> = [B1,B2]
                # L ---> B1, B2, b3
                # 50% => b2 


                ## pour le classement
                ## crank : author, title