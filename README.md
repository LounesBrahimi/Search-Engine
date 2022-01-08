# daar-final-project

### commandes : NB : on peut développer un script pour executer ces commandes d'un coup...

- décommenter la ligne 2 et 3 du fichier tools.py pour télécharger les stopword.. 
- pip install pydantic
- python manage.py makemigrations
- python manage.py migrate  
- python manage.py dataLoader 1 
- python manage.py runserver

NB : commenter les deux lignes (tools.py) après le lancement du serveur 

### exemple de requetes : 

- http://127.0.0.1:8000/gelAllBooks/
- http://127.0.0.1:8000/gelAllIndex/
- http://127.0.0.1:8000/Books/Search/11/
- http://127.0.0.1:8000/Index/Search/Modern/
- http://127.0.0.1:8000/Index/Search/Wonderland/

## Moteur de recherche d’une bibliotheque.

Il s’agit de proposer une application web/mobile de moteur de recherche de document dans une bibliotheque de livres sous format textuel. Pour cela, la premiere étape est de s’occuper de la couche ´ data du projet, i.e. la construction d’une bibliotheque personnelle de livres, stockées sous forme de documents textuels. La taille minimum de la bibliotheque doit etre ˆ 1664 livres. La taille minimum de chaque livre doit etre 10000 (dix mille) mots. Dans un second temps, il s’agit de construire une application web/mobile (couches serveur et client) afin de munir sa bibliotheque d’un moteur de `
recherche. Chaque groupe est libre de determiner la présentation frontend et les userstory de son application, cependant,
les fonctionnalites principales de l’application doivent obligatoirement comprendre :

### Une fonctionnalite explicite de “Recherche”

- Recherche de livre par mot-clef. A la suite d’une entree texte S de l’utilisateur, l’application retourne la liste de tous les documents textuels dont la table de l’indexage contient la chaıne de caracteres S

### Une fonctionnalite explicite de “Recherche avancée”

- Recherche dite “avancee” de livre par RegEx. A la suite d’une entree texte RegEx de l’utilisateur, l’application retourne : soit la liste de tous les documents textuels dont la table de l’indexage contient une chaˆıne de caracteres S qui verifie l’expression reguliere RegEx; soit la liste de tous les documents textuels dont le contenu textuel contient une chaˆıne de caracteres S qui verifie l’expression reguliere RegEx (attention a la d`egradation en performance).

###  Une fonctionnalite implicite de classement : 


### Une fonctionnalite implicite de suggestion :



- ...


