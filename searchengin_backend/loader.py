from searchengin_backend.models import BookM
import requests

from searchengin_backend.serializers import BookSerializer

class Loader():

    def handler():
        
        ##
        api_url = "https://gutendex.com/"
        myurl = "http://127.0.0.1:8000/"
        nbPage = 20
        map_book = {}
        
        ###
        for i in range(1, nbPage):
            response = requests.get(api_url+'/books?mime_type=text&'+'page='+str(i))
            jsondata = response.json()
            data = jsondata['results']

            for book in data :
                body = book['formats']["text/plain; charset=utf-8"]
                serializer = BookSerializer(data = {
                    "id": book['id'],
                    "title": book['title'],
                    "author": ('None' if len(book['authors']) == 0 else book['authors'][0]['name']),
                    "body": body,
                    "lang": book['lang'][0]
                }
                )

                ### ....
                serializer.save()
                ### ..


