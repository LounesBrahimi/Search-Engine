from django.test import TestCase
from searchengin_backend.models import BookM, BookMIndex, JaccardGraph
from searchengin_backend.serializers import BookMSerializer, JaccardGraphSerializer
from searchengin_backend.utils import calculJaccardDistance, getWordList
from collections import Counter

# là j'ai presque terminer les tests unitaires
class Test(TestCase):
    b1 = {
        "id": "30",
        "title": "daar final project one",
        "author": "oussama",
        "lang": "english",
        "cover": "sorry, cover not available",
        "body": "daar final project is a search engine...etc"
    }

    b2 = {
        "id": "30",
        "title": "daar final project two",
        "author": "lounes",
        "lang": "english",
        "cover": "sorry, cover not available",
        "body": "daar final project is a search engine...etc"
    }

    def test_bookTest(self):
      serializer = BookMSerializer(data=self.b1)
      if (serializer.is_valid()):
          serializer.save()
          book = BookM.objects.filter(id="30")
          self.assertEqual(len(book), 1)

    def test_graphTest(self):
      for i in range(2):

        serializerb1 = BookMSerializer(data=self.b1)
        serializerb2 = BookMSerializer(data=self.b2)
        if(serializerb1.is_valid()):
          serializerb1.save()
        if(serializerb2.is_valid()):
          serializerb2.save()

        wordsb1 = getWordList(self.b1['title'] , self.b1['lang'])
        wordsb2 = getWordList(self.b2['title'] , self.b2['lang'])

        d1 = calculJaccardDistance(Counter(wordsb1)  , Counter(wordsb2))
        d2 = calculJaccardDistance(Counter(wordsb2)  , Counter(wordsb1))
        
        serializerGraph = JaccardGraphSerializer( data = {
                          "bookId"    : self.b1['id'],
                          "neighbors" : [self.b2['id']],
                          "totalDistance" : d1
                      }
        )
        if(serializerGraph.is_valid()):
          serializerGraph.save()

        # bookgraph = JaccardGraph.objects.filter(id="30")
        self.assertEqual(d1,d2)