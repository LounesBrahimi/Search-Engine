#!/usr/bin/python

import sys
import subprocess

def run_command(command):
    p = subprocess.Popen(command,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def main():
    if (len(sys.argv) < 3):
        print("Erreur : veuillez introduire l'expression reguliere et le text")
    elif((len(sys.argv[1]) == 0) | (len(sys.argv[2]) == 0)):
        print("Erreur : veuillez introduire l'expression reguliere  et le text")
    else:
        for output_line in run_command(['java', '-jar', 'regExSearch.jar', sys.argv[1], sys.argv[2]]):
            print(output_line)


main()
