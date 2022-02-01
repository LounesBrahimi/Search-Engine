import requests
import html2text

from searchengin_backend.serializers import BookMSerializer

url_online_db = "https://gutendex.com/"

def numberWordOfString(text : str):
    word_list = text.split()
    return len(word_list)

def contructDB(sizeDB: int, minNumberWords: int):
    numberBooksStocked : int = 0
    
    page_num : int = 0
    while (numberBooksStocked < sizeDB):
            page_num += 1
            list_books = requests.get(url_online_db+'/books?mime_type=text&'+'page='+str(page_num))
            list_books_json = list_books.json()
            data = list_books_json['results']
            for book in data:
                textBook : str = ""
                if (numberBooksStocked > sizeDB):
                    break
                url_book = book['formats']['text/html']
                book_html = requests.get(url_book).text
                h = html2text.HTML2Text()
                h.ignore_links = True
                textBook = h.handle(book_html)
                numberWords : int = numberWordOfString(textBook)
                if (numberWords >= minNumberWords):
                    numberBooksStocked += 1
                    serializer = BookMSerializer(data = {
                        "id": book['id'],
                        "title": book['title'],
                        "author": ('None' if len(book['authors']) == 0 else book['authors'][0]['name']),
                        "lang": book['lang'],
                        "body": textBook
                        })
                    serializer.save()
                    print(str(numberBooksStocked)+" stocked")

sizeDB : int = 1664
minNumberWords : int = 10000
contructDB(sizeDB, minNumberWords)