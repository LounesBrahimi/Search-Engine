from asyncio.windows_events import NULL
from signal import raise_signal
from SyntaxTree import SyntaxTree

class RegEx:
    
    CONCAT = 0xC04CA7
    ETOILE = 0xE7011E
    ALTERN = 0xA17E54
    PROTECTION = 0xBADDAD
    PARENTHESEOUVRANT = 0x16641664
    PARENTHESEFERMANT = 0x51515151
    DOT = 0xD07
    
    def __init__(self, regEx: str):

        # Expression reguliere
        self.regEx = regEx
    
    # Convertie l'expression reguliere en un arbre syntaxique
    def parse1(self):
        result = []
        for i in range(0, len(self.regEx), +1):
            if (self.regEx[i] != '.'):
                result.append(SyntaxTree(self.charToRacine(self.regEx[i]), []))
        return self.parse(result)


    #Convertie les caracteres en macros
    def charToRacine(self, c: str):
        if (c=='.'):
            return self.DOT
        elif (c=='*'):
            return self.ETOILE
        elif (c=='|'):
            return self.ALTERN
        elif (c=='('):
            return self.PARENTHESEOUVRANT
        elif (c==')'):
            return self.PARENTHESEFERMANT
        else:
            return ord(c)

    def parse(self, result):
        while (self.containParenthese(result)):
            result = self.processParenthese(result)
        while (self.containEtoile(result)):
            res = self.processEtoile(result)
            result = []
            result = res
        while (self.containConcat(result)):
            res = self.processConcat(result)
            result = []
            result = res
        while (self.containAltern(result)):
            result = self.processAltern(result)
        if (len(result)>1):
            raise ValueError('Error in parse')
        res = []
        res = self.removeProtection(result[0])
        return res
    
    # Verifie si la liste d'arbres syntaxiques contient des parentheses
    def containParenthese(self, trees):
        for t in trees:
            if ((t.getRacine() == self.PARENTHESEFERMANT) | (t.getRacine() == self.PARENTHESEOUVRANT)):
                return True
        return False

    # Cherche et detecte les arbres positionner entre les deux arbres avec une racine respectivement
    # (PARENTHESEOUVRANT et PARENTHESEFERMANT), l'algorithme supprime ces deux derniers arbres 
    # et traite la traite la suite d'arbres qu'ils délimitaient, 
    def processParenthese(self, trees):
        result = []
        found: bool = False
        for t in trees:
            if ((not found) & (t.getRacine() == self.PARENTHESEFERMANT)):
                done: bool = False
                content = []
                while ((not done) & (not(len(result) == 0))):
                    if (result[len(result)-1].getRacine() == self.PARENTHESEOUVRANT):
                        done = True
                        del result[len(result)-1]
                    else:
                        content.append(result[len(result)-1])
                        del result[len(result)-1]
                if (not done):
                    raise ValueError('processParenthese')
                found = True
                subTrees = []
                subTrees.append(self.parse(content))
                result.append(SyntaxTree(self.PROTECTION, subTrees))
            else:
                result.append(t)
        if (not found):
           raise ValueError('processParenthese 2')
        return result

    # Verifie si la liste d'arbres syntaxiques contient l'etoiles
    def containEtoile(self, trees):
        for t in trees:
            if ((t.getRacine() == self.ETOILE) & ((len(t.getSousArbre()) == 0))):
                return True
        return False

    # Cherche et detecte la liste des arbres positionnés avant l'arbre dont la racine est étoile
    # cette liste d'arbre deviennent le sous arbres de l'étoile 
    def processEtoile(self, trees):
        result = []
        found: bool = False
        for t in trees:
            if (((not found) & (t.getRacine() == self.ETOILE)) & (len(t.getSousArbre()) == 0)):
                if (len(result) == 0):
                    raise ValueError('processEtoile')
                found = True
                last = result[len(result)-1]
                del result[len(result)-1]
                subTrees = []
                subTrees.append(last)
                result.append(SyntaxTree(self.ETOILE, subTrees))
            else:
                result.append(t)
        return result

    # Verifie si la liste d'arbres syntaxiques contiennent la concaténation
    def containConcat(self, trees):
        firstFound: bool = False
        if (len(trees)==0):
            return False
        for t in trees:
            if ((not firstFound) & (t.getRacine()!=self.ALTERN)):
                firstFound = True
                continue
            if (firstFound):
                if (t.getRacine()!=self.ALTERN):
                    return True
                else:
                    firstFound = False
        return False
    
    # Dans le cas de deux arbres qui ce suivent sans altérnation, la méthode prend 
    # le premier noeud, puis le deuxieme, et ces deux arbres deviennent les fils d'un nouveau
    # noeud représentant la concaténation

    def processConcat(self, trees):
        result = []
        found = False
        firstFound = False
        for t in trees:
            if (((not found) & (not firstFound)) & (t.getRacine()!=self.ALTERN)):
                firstFound = True
                result.append(t)
                continue
            if (((not found) & firstFound) & (t.getRacine()==self.ALTERN)):
                firstFound = False
                result.append(t)
                continue
            if (((not found) & firstFound) & (t.getRacine()!=self.ALTERN)):
                found = True
                last = result[len(result)-1]
                del result[len(result)-1]
                subTrees = []
                subTrees.append(last)
                subTrees.append(t)
                result.append(SyntaxTree(self.CONCAT, subTrees))
            else:
                result.append(t)
        return result

    # Verifie si la liste d'arbres syntaxiques contiennent une alternation
    def containAltern(self, trees):
        for t in trees:
            if((t.getRacine() == self.ALTERN) & (len(t.getSousArbre()) == 0)):
                return True
        return False

    # Détecte la gauche de l'arbre a la racine altern, ce dernier deviens son fils gauche,
    # la méthode et continue et détecte sa droite et deviens ainsi son fils gauche
    def processAltern(self, trees):
        result = []
        found: bool = False
        gauche: SyntaxTree = NULL
        done: bool = False
        for t in trees:
            if (((not found) & (t.getRacine()==self.ALTERN)) & (len(t.sousArbre) == 0)):
                if (len(result) == 0):
                    raise ValueError('processAltern')
                found = True
                gauche = result[len(result)-1]
                del result[len(result)-1]
                continue
            if (found & (not done)):
                if (gauche==NULL):
                    raise ValueError('processAltern 2')
                done = True
                subTrees = []
                subTrees.append(gauche)
                subTrees.append(t)
                result.append(SyntaxTree(self.ALTERN, subTrees))
            else:
                result.append(t)
        return result
    
    # Supprime l'arbre protection mis pendant le traitement des parentheses
    def removeProtection(self, tree):
        if ((tree.getRacine() == self.PROTECTION) & (len(tree.sousArbre) != 1)):
            raise ValueError('removeProtection')
        if (len(tree.getSousArbre()) == 0):
            return tree
        if (tree.getRacine() == self.PROTECTION):
            return self.removeProtection(tree.getSousArbre()[0])
        subTrees = []
        for t in tree.getSousArbre():
            subTrees.append(self.removeProtection(t))
        return SyntaxTree(tree.getRacine(), subTrees)
