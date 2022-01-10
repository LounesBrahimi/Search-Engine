
## commandes : NB : on peut développer un script pour executer ces commandes d'un coup...

décommenter la ligne 2 et 3 du fichier tools.py pour télécharger les stopword.. puis commenter-les
pip install pydantic
python manage.py makemigrations
python manage.py migrate  
python manage.py dataLoader 1 
python manage.py runserver

## requetes : 

http://127.0.0.1:8000/gelAllBooks/
http://127.0.0.1:8000/gelAllIndex/
http://127.0.0.1:8000/Books/Search/11/
http://127.0.0.1:8000/Index/Search/Modern/
http://127.0.0.1:8000/Index/Search/Wonderland/
...
