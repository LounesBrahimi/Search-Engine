import requests

url_online_db = "https://gutendex.com/"

def contructDB(sizeDB: int):
    numberBooksStocked : int = 0
    
    page_num : int = 0
    while (numberBooksStocked < sizeDB):
            page_num += 1
            list_books = requests.get(url_online_db+'/books?mime_type=text&'+'page='+str(page_num))
            list_books_json = list_books.json()
            data = list_books_json['results']

            for book in data :
                if (numberBooksStocked > sizeDB):
                    break
                print(book)
                print("\nnumber ## "+str(numberBooksStocked)+" ##\n")
                numberBooksStocked += 1


sizeDB : int = 10
contructDB(sizeDB)