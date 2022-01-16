from asyncio.windows_events import NULL


class KmpAlgorithm:

    def __init__(self, regEx: str, text: str):

        # Expression reguliere
        self.regEx = regEx
        # Le text dans lequel effectuer la recherche
        self.text = text
        # Une liste ordonée des caractères de l'expression reguliere
        self.Factor = []
        # Une liste indiquant pour chaque position un décalage
        self.CarryOver = []

    # Convertie l'expression reguliere en une liste ordonée des caractères
    # (crée le Factor)
    def generateFunctor(self):
        for i in range(len(self.regEx)):
            self.Factor.insert(i, self.regEx[i])
    
    # Retourne la premiere partie de Factor de 0 à l'indice passé
    # en paramètre
    def getFirstPart(self, indice:int):
        firstPart = []
        for i in range(indice):
            firstPart.insert(i, self.Factor[i])
        return firstPart
    
    # Prend une ligne et un indice et retourne un suffixe de cette ligne en utilisant
    #l'indice
    def getSuffixFromN(self, s: str, n: int):
        length : int= len(s)
        result : str = s[(length-n):(length)]
        result
    
    # Methode qui convertie une liste de chaine de caractère en une chaine
    # de caractère unique et cela en faisant la concatenation.
    def listToString(self, s):
        result = ''.join(s)
        return result
    
    # Verifie si le suffixe passé en parametre est aussi un préffixe
    # de la chaine.
    def isPreffix(self, chaine: str, suffix: str):
        if suffix == None :
            False
        else:
            chaine.startswith(suffix)
    
    # Methode qui retourne la taille du plus long suffixe propre qui est aussi
    # un préfixe
    def getLengthLongestProperSuffixPreffix(self, s):
        chaine :str = self.listToString(s)
        for i in range((len(chaine)-1), 0,-1):
            suffix: str = self.getSuffixFromN(chaine, i)
            if (self.isPreffix(chaine, suffix)):
                return len(suffix)
        return 0
    
    # La methode génère une liste nommée « Carry Over » qui indique 
    # pour chaque position un décalage à effectuer si la chaine de 
    # caractère ne match pas à partir d’un certain indice.
    def generateCarryOver(self):
        self.CarryOver.append(-1)

        for i in range(1, len(self.regEx), +1):
            firstPart = self.getFirstPart(i)
            if (len(firstPart) == 1):
                self.CarryOver.append(0)
            else:
                value: int = self.getLengthLongestProperSuffixPreffix(firstPart)
                self.CarryOver.append(value)
        
        for i in range(1, len(self.Factor), +1):
            if ((self.Factor[i] == self.Factor[0]) & (self.CarryOver[i] == 0)):
                self.CarryOver[i] = -1
        
        for i in range(0, len(self.Factor), +1):
            if ( (self.CarryOver[i] != -1) & (self.Factor[i] == (self.Factor[self.CarryOver[i]]) ) ):
                self.CarryOver[i] = self.CarryOver[self.CarryOver[i]]
        
        self.CarryOver.append(0)

    # Methode qui divise une unique chaine de caractere en une liste
    # de chaines de caracteres representant les lignes.
    def textToLines(self):
        return self.text.split("\n")
    
    # Cherche dans tout les suffixes de la ligne passée en parametre
    # en prenant soin de faire les décalages dans les cas de crash
    # en utilisant le Carry Over
    # renvoie cette derniere si elle match et qu'il n'ya pas de crash
    def searchInAllSuffixs(self, line: str):
        i: int = 0
        while ((i < len(line)) & ((len(line) - i) >= len(self.Factor))):
            crashIndice: int = 0
            for j in range(0, len(self.Factor), +1):
                if (self.Factor[j] == (""+line[j+i])):
                    crashIndice = crashIndice + 1
            
            if (crashIndice == len(self.Factor)):
                return line
            else:
                i = i + crashIndice - self.CarryOver[crashIndice]
        return NULL

    # Methode qui fait la recherche de la chanine de caractere
    # dans le texte.
    def search(self):
        textLines = self.textToLines()
        listResults = []
        for i in range(0, len(textLines), +1):
            result: str = self.searchInAllSuffixs(textLines[i])
            if (result != NULL):
                listResults.append(result)
        return listResults

