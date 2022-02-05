import nltk
# nltk.download('stopwords') 
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from searchengin_backend.serializers import BookMIndexSerializer
import math 

jaccardDistance = 90 ## distance de jaccard en %

# récuperer la liste des stop words 
def getStopWordList(lang):
    if lang == "en":
        lang = "english"
    elif lang == "fr":
        lang = "french"
    return set(stopwords.words(lang))

# renvoyer une liste des mots dans un texte en supprimant les stopword, les espaces, les mots non utils...
def getWordList(text,lang) : 
    stop_words = getStopWordList(lang)
    text = text.lower()
    words = word_tokenize(text)
    filtered_words = []    
    for w in words:
        if w not in stop_words:     
            filtered_words.append(w)

    filtered_words = [w for w in words if len(w) > 2
                                                and w != ''
                                                and not w.lower() in stop_words]
    return filtered_words

# serializer la table d'indexage
def serializeIndex(self,indexbject,counter):
    # self.stdout.write('index table : '+str(indexbject)+'\n')
    serializerIndex = BookMIndexSerializer(data={
            "attributes":indexbject
        }
    )
    if serializerIndex.is_valid(raise_exception=True):
        serializerIndex.save()
        self.stdout.write(self.style.SUCCESS(' >> sucess adding index : '+str(counter)))
    else :
        self.stdout.write(self.style.ERROR(' >> sucess adding index : '+str(counter)))                 
    print("\n")

# afficher un livre      
def printBook(self,idBook,counter):
    self.stdout.write('book '+str(counter)+' / book id : "%s"' % idBook)

def printSuccesMessage(self,message):
    self.stdout.write(self.style.SUCCESS(message))

def printErrorMessage(self,message):
    self.stdout.write(self.style.ERROR(message))

# sauvgarder le graphe
def saveGraph(serializerGraph):
    if serializerGraph.is_valid(raise_exception=True):
        serializerGraph.save()
    else :
        print(' >> error adding graph')

# vérifier qu'un livre respecte la distance de jaccard
def verifyJaccardDistance(dist, neighborId, neighbors):
    if math.floor(dist) < jaccardDistance: 
        print(" >> add this neighbour : "+str(neighborId)+"\n")
    else:
        print(" >> do not add this neighbour : "+str(neighborId))
        neighbors.remove(neighborId)

# calculer la distance de jaccard entre deux noeuds/livres dans le graphe
def calculJaccardDistance(wordsb1,wordsb2):
    sumOfOcc    = 0
    sumOfmaxOcc = 0
    # word exist just in b1 and b2 : 
    common_words = set(wordsb1).intersection(wordsb2)
    for w1 in common_words:
        occb1 = wordsb1[w1]
        occb2 = wordsb2[w1]
        sumOfmaxOcc +=  max(occb1,occb2) - min(occb1,occb2)
        sumOfOcc    +=  max(occb1,occb2)
    # word exist just in b1 : 
    inb1 = list(set(wordsb1).difference(wordsb2))
    for w2 in inb1:
        sumOfmaxOcc += wordsb1[w2]
        sumOfOcc    += wordsb1[w2]
    # word exist just in b2
    inb2 = list(set(wordsb2).difference(wordsb1))
    for w3 in inb2:
        sumOfmaxOcc += wordsb2[w3]
        sumOfOcc    += wordsb2[w3]
    try:
        return sumOfmaxOcc/sumOfOcc
    except:
        return 1

# afficher la distance de jaccard
def printDistance(bookPertinentId, neighborId, dist):
    print(" >> distance between "+str(bookPertinentId)+" and "+str(neighborId)+" is : "+str(round(dist,2))+" ")

# supprimer un clé depuis un dictionnaire
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

# renvoyer le nombre des mots dans une chaine (espace comme séparateur) 
def numberWordOfString(text : str):
    word_list = text.split()
    return len(word_list)