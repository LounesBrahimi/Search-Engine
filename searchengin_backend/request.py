# import requests module
# installer : pip3 install django djangorestframework requests
import requests
 
## response = requests.get('https://gutenberg.org/files/56673/56673-h/56673-h.htm')
## https://gutendex.com//books?mime_type=text&page=2

api_url = "https://gutendex.com/"
pages_web_num = 4 ## nombre de page web => chaque page web contient 32 livres

 ## pour avoir 1664 il faut parcourir 52 page web
while(pages_web_num*32 % 1664 != 0) :
    pages_web_num = pages_web_num + 1
        
print("-----")
print(pages_web_num)
print("-----")

for i in range(1, 2): 
    ## mime_type permet de trouver les livres avec un type donnée
    response = requests.get(api_url+'/books?mime_type=text&'+'page='+str(i)) ## voila il est utilisé
    jsondata = response.json()
    books = jsondata['results']   

    ## books [ {} , {} , {} , {} , {}] = [ 34 books ]

    ## print(len(books)) --> 32
    x = 0
    for book in books: ## pour chaque livre
        x = x+1
        id = book['id']
        title = book['title']
        author = ('unknown' if len(book['authors']) == 0 else book['authors'][0]['name'])
        language = book['languages'][0]

        try:
            text = book['formats']["text/plain; charset=utf-8"]
            text = text.replace(".zip", ".txt")
        except:
            continue
        
         # print json content
        print("id = ",id)
        print("title = ",title)
        print("author = ",author)
        print("lang = ",language)
        print("text = ",text)
        print(" ---- ")
        print(x)
