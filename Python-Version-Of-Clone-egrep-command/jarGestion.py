#!/usr/bin/python

import sys
import subprocess

def main():
    if (len(sys.argv) < 3):
        print("Erreur : veuillez introduire l'expression reguliere et le fichier txt")
    elif((len(sys.argv[1]) == 0) | (len(sys.argv[2]) == 0)):
        print("Erreur : veuillez introduire l'expression reguliere et le fichier txt")
    else:
        print("____________________________________")
        print("regEx : "+ sys.argv[1])
        subprocess.call(['java', '-jar', 'regExSearch.jar', sys.argv[1], sys.argv[2]])

main()