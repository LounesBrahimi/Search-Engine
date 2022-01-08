import nltk
# nltk.download('stopwords') 
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from searchengin_backend.serializers import BookMIndexSerializer


# recuperer la liste des stop words 
def getStopWordList(lang):
    if lang == "en":
        lang = "english"
    elif lang == "fr":
        lang = "french"

    return set(stopwords.words(lang))

# renvoyer une liste des mots dans un texte en supprimant les stopword, les espaces, les mots non utils...
def getWordList(text,lang) : 
    stop_words = getStopWordList(lang)
    words = word_tokenize(text)
    filtered_words = []
    
    for w in words:
        if w not in stop_words:
            filtered_words.append(w)

    filtered_words = [w for w in words if len(w) > 2
                                                and w != ''
                                                and not w.lower() in stop_words]
    return filtered_words


# textsample = "J suis un exemple de texte"
# print(getWordList("french",textsample))

# 
def serializeIndex(self,indexbject,counter):
    self.stdout.write('index table : '+str(indexbject)+'\n')
    serializerIndex = BookMIndexSerializer(data={
            "attributes":indexbject
        }
    )

    if serializerIndex.is_valid(raise_exception=True):
        serializerIndex.save()
        self.stdout.write(self.style.SUCCESS(' ------> sucess adding index : '+str(counter)))
    else :
        self.stdout.write(self.style.ERROR(' ------> sucess adding index : '+str(counter)))
                      
    print("\n")

               
def printBook(self,idBook,title,author,lang,body,counter):
    self.stdout.write('book '+str(counter)+' / book id : "%s"' % idBook)
    #self.stdout.write('title : "%s"' % title)
    #self.stdout.write('book author : "%s"' % author)
    #self.stdout.write('book lang : "%s"' % lang)
    #self.stdout.write('book text : "%s"' % body)


def printSuccesMessage(self,message):
    self.stdout.write(self.style.SUCCESS(message))

def printErrorMessage(self,message):
    self.stdout.write(self.style.ERROR(message))
