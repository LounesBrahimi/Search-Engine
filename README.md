# daar-final-project

### commandes :

commencer par créer un environnement python, ensuite :

pour le backend : 
- se deplacer dans le projet daarproject-backend

- décommenter la ligne 2 et 3 du fichier tools.py pour télécharger les stopword (a commenter une fois)
- pip3 install django djangorestframework
- pip install pydantic
- pip install nltk

- python manage.py makemigrations 
- python manage.py migrate  
- python manage.py dataLoader 
- python manage.py runserver

pour le front : 
- se déplacer dans le projet daarproject-backend
- npm install
- ng serve

NB : commenter les deux lignes (utils.py) après le lancement du serveur 

### requetes pour tester le fonctionnement du projet :
- http://127.0.0.1:8000/getAllBooks
- http://127.0.0.1:8000/getAllIndex/
- http://127.0.0.1:8000/getGraph/
- http://127.0.0.1:8000/Books/<str:id>/
- http://127.0.0.1:8000/Books/Search/<str:word>/


### algorithme de suggestions :
- conserver que dix livres 
- suite à une recherche, récuperer les 3 livres les plus pertinents de la recherche : qui contient le + grand nombre d'occ du mot clé 
- pour chacun des 3 livres, récuperer tt les voisins possibles (les voisins qui restent de la recherche)
- selectionner que les voisins qui vérifient la distance de jaccard
- stocker dans le graphe le livre pertinant et l'arret vers ses voisins + les arrêts inversés
- si le livre pertinent est déja existe dans le graphe mettre à jour la liste de ses voisins ainsi que la distance total de chaque noeuds 
  vers tous les autres noeuds du graphe

### algorithme de classement : 
- calculer pour chaque noeuds son centralité dans le graphe de jaccard.
- mettre à jour le classement des livre après chaque recherche (closeness algo) 

### Moteur de recherche d’une bibliotheque.

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
