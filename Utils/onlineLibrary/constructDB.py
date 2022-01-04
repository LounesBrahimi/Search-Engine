import urllib.request

def numberWordOfString(text : str):
    word_list = text.split()
    return len(word_list)

def contructDB(bookId: int, sizeDB: int, minNumberWords: int):
    numberBooksStocked : int = 0
    textBook : str = ""
    while (numberBooksStocked < sizeDB):
        bookIdStr = str(bookId)
        try:
            with urllib.request.urlopen("https://gutenberg.org/files/"+bookIdStr +"/"+
                                bookIdStr+"-h/"+bookIdStr+"-h.htm") as url:
                textBook = url.read().decode('utf-8')
                numberWords : int = numberWordOfString(textBook)
                if (numberWords >= minNumberWords):
                    numberBooksStocked += 1
                    print(numberWords)
                    print(len(textBook))
        except:
            pass
        bookId += 1


sizeDB : int = 10
minNumberWords : int = 10000
bookInitialId : int = 56667
contructDB(bookInitialId, sizeDB, bookInitialId)