#!/usr/bin/python

import sys

from KmpAlgorithm import KmpAlgorithm
from RegEx import RegEx
from SyntaxTree import SyntaxTree
from NDFA import NDFA

#Retourne vraie si l'expression reguliere est reduite à une suite de concatenations
def estSuiteConcatenations(regEx : str):
    for i in range(len(regEx)):
        if (((regEx[i] == '*') | (regEx[i] == '|')) | (regEx[i] == '.')):
            return False
    return True

# Ouvre le fichier avec le nom "fileName" passé en parametre, recupere
# le texte dans le fichier et le retourne
def fileToText(fileName : str):
    f = open(fileName, "r")
    return f.read()

# Methode qui imprime la matrice representant un automate

# Methode qui imprime sur la sortie standard les lignes résutants de la
# recherche mené avec l'une des deux methodes.
def printLignes(lignes):
    for ligne in lignes:
        print(ligne)

# Methode qui imprime la matrice representant un automate
def printMatrix(ndfaMatrix):
    for i in range(0, 259, +1):
        for j in range(65, len(ndfaMatrix[i]), +1):
            if (((j > 64) & (j < 123)) | (j > 250)):
                print(str(ndfaMatrix[i][j]) + " ",  end='', flush=True)
        print("")

def main():
    if (len(sys.argv) < 3):
        print("Erreur : veuillez introduire l'expression reguliere et le fichier txt")
    elif((len(sys.argv[1]) == 0) | (len(sys.argv[2]) == 0)):
        print("Erreur : veuillez introduire l'expression reguliere et le fichier txt")
    else:
        print("____________________________________")
        print("regEx : "+ sys.argv[1])
        print("____________________________________")
        if (estSuiteConcatenations(sys.argv[1])):
            print("=========Recherche avec KMP=========")
            regEx : str = sys.argv[1]
            text : str = fileToText(sys.argv[2])
            kmp = KmpAlgorithm(regEx, text)
            kmp.generateFunctor()
            kmp.generateCarryOver()
            printLignes(kmp.search())
        else:
            print("=========Recherche avec automate=========")
            regEx : str = sys.argv[1]
            r = RegEx(regEx)
            # Conversion de l'expression réguliere en arbre syntaxique
            ret: SyntaxTree = r.parse1()
            print(ret.toString())
            n = NDFA(100000)
            n.arbreToNDFA(ret)
            printMatrix(n.getNdfaMatrix())

main()