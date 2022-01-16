class SyntaxTree:

    CONCAT = 0xC04CA7
    ETOILE = 0xE7011E
    ALTERN = 0xA17E54
    PROTECTION = 0xBADDAD
    PARENTHESEOUVRANT = 0x16641664
    PARENTHESEFERMANT = 0x51515151
    DOT = 0xD07

    def __init__(self, racine: int, sousArbre):

        self.racine = racine
        self.sousArbre = sousArbre

    # Convert the value of the root to String
    def racineToString(self):

        if (self.racine == self.CONCAT):
            return "."
        elif (self.racine == self.ETOILE):
            return "*"
        elif (self.racine == self.ALTERN):
            return "|"
        elif (self.racine == self.DOT):
            return "."
        else:
          #  print(self.racine)
            return self.racine

    # Convert tree to parenthesis
    def toString(self):
        if (len(self.sousArbre) == 0):
             return chr(self.racineToString())
        print("###")   
        print(str(self.racineToString())) 
        print("###")      
        result: str = str(self.racineToString())+"("+str(self.sousArbre[0].toString())
        for i in range(1, len(self.sousArbre), +1):
            result+=","+str(self.sousArbre[i].toString())
        return result+")"
    
    def getRacine(self):
        return self.racine

    def getSousArbre(self):
        return self.sousArbre