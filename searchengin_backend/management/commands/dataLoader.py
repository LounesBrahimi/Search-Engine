from django.core.management.base import BaseCommand, CommandError
from searchengin_backend.validator import AttributesSchema
from searchengin_backend.models import BookM, BookMIndex
from searchengin_backend.serializers import BookMSerializer
import requests


from searchengin_backend.utils import getWordList, printBook, printErrorMessage, printSuccesMessage, serializeIndex

class Command(BaseCommand):

    ## declarations
    help = 'Load data from api'

    ## ajouter un argument à la commande
    def add_arguments(self, parser): 
        parser.add_argument('page_id', nargs='+', type=int)

    ## fonction principal handler 
    def handle(self, *args, **options) :

        ## init
        api_url = "https://gutendex.com/"
        pages_web_num = 4 
        counter = 0
        bookMap = {}

        ## ----------------------
        sizeDB : int = 1664
        minNumberWords : int = 10000
        numberBooksStocked : int = 0

        ## -----------------------
        
        # supprimer les anciens données enregistrées
        BookM.objects.all().delete()
        BookMIndex.objects.all().delete()

        ## recuperer le parametre
        p_num = options['page_id']
        self.stdout.write('numero de page web : "%s"' % p_num)

        ## pour avoir 1664 il faut parcourir 52 page web
        # while(pages_web_num*32 % nbBook != 0) :
        #         pages_web_num = pages_web_num + 1
    
        for i in p_num: ## pour chaque page web on recupere 32 books => 2*32 = 64
            
            self.stdout.write(self.style.SUCCESS('-------- page web id : '+str(i)+' --------'))

            # recuperer tt les livres
            response = requests.get(api_url+'/books?mime_type=text&'+'page='+str(i))
            jsondata = response.json()
            books = jsondata['results']

            for book in books: ## pour chaque livre
                # words = re.findall('[a-zA-Z\u00C0-\u00FF]*', body) ## attention : body = url vers le texte
                # if len(words) < 10000:
                #     continue
                # else : 
                    counter  = counter + 1
                    # if (numberBooksStocked > sizeDB):
                    #     break
                    # ------------- contruire la table des livres  ------------- #
                    
                    idBook = book['id']
                    title = book['title']
                    author = ('unknown' if len(book['authors']) == 0 else book['authors'][0]['name'])
                    lang = book['languages'][0]
                    try:
                        body = book['formats']["text/plain; charset=utf-8"]
                        body = body.replace(".zip", ".txt")
                    except:
                        continue
                    
                    # afficher le contenu d'un livre
                    printBook(self,idBook,title,author,lang,body,counter)

                    # serializer la table des livres
                    serializer = BookMSerializer(data = {
                            "id":idBook,
                            "title":title,
                            "author":author,
                            "lang":lang,
                            "body": body
                        }
                    )

                    if serializer.is_valid(raise_exception=True):
                        serializer.save() 
                        printSuccesMessage(self,' ------> sucess adding book : '+str(idBook))

                        # ------------- contruire la table d'indexage  ------------- #
                        
                        ## 1 - recupérer la liste des mots du titre, pour l'instant on suppose que la recherche fait par titre
                        text_response = title+" ".join(book['subjects'])
                        words = getWordList(text_response,lang)

                        ## 2 - contruire l'objet index pour chaque livre 
                        indexbject = {
                                'idIndex': counter,
                                'idBook' : idBook,
                                'words': words,
                        }
                        
                        bookMap[idBook] = words

                        ## 3 - validation des données
                        AttributesSchema(**indexbject)

                        ## 4 - serializer la table d'indéxage 
                        serializeIndex(self,indexbject,counter)
                    else:
                        printErrorMessage(self,' ------> error adding book with id : "%s"'% id)
                    

