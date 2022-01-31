from asyncio.windows_events import NULL


class NDFARemoveEpsilon:
    
    # Indique à temps reel le numero d'un etat non existant et qu'on peut donc creer
    numeroEtat: int = 0

    CONCAT = 0xC04CA7
    ETOILE = 0xE7011E
    ALTERN = 0xA17E54
    PROTECTION = 0xBADDAD
    PARENTHESEOUVRANT = 0x16641664
    PARENTHESEFERMANT = 0x51515151
    DOT = 0xD07

    def __init__(self, ndfaMatrix, nLignes: int, nColonnes, numeroEtat):
        # Nombre de lignes de la matrice
        self.nLignes = nLignes
        # Nombre de colonnes de la matrice
        self.nColonnes = nColonnes
        # La matrice representant l'automate finie non deterministe
        self.ndfaMatrix = ndfaMatrix
        # La matrice representant l'automate sans epsilons transitions
        self.nouveauNdfaMatrix = [ [ 0 for i in range(self.nLignes) ] for j in range(self.nColonnes) ]
        # la colonne 256 indique si l'etat a des epslions transitions
        self.indiceEpsilon = 256
	    # la colonne 257 indique si l'etat est un etat initiale
        self.indiceInitiale = 257
	    # la colonne 257 indique si l'etat est un etat finale
        self.indiceFinale = 258

        self.numeroEtat = numeroEtat

    # Méthode qui supprime les epsilons transitions et stock l'automate obtenue dans
    # nouveauNdfaMatrix
    def supression(self):
        nonEtatPuit = set(())
        #ajout de l'etat intiale
        nonEtatPuit.add(0)
        for i in range(0, len(self.ndfaMatrix)):
            print(len(self.ndfaMatrix))
            if (self.ndfaMatrix[i][self.indiceEpsilon] == NULL):
                #si l'état courant n'a pas d'epsilon transition sorant
                self.nouveauNdfaMatrix[i] = self.ndfaMatrix[i]
                for j in range(0, self.nColonnes-3):
                    if ((self.ndfaMatrix[i][j] != NULL) & (j != self.indiceEpsilon)):
                        for x in range(0, len(self.ndfaMatrix[i][j])):
                            nonEtatPuit.add(self.ndfaMatrix[i][j][x])
            else:
                #si l'état courant a des epsilons transitions sorants
                lEtatsMemeGroupe = []
                for x in range(0, len(self.ndfaMatrix[i][self.indiceEpsilon])):
                    lEtatsMemeGroupe.append(self.ndfaMatrix[i][self.indiceEpsilon][x])
                    etat_pointe_epsilon = self.ndfaMatrix[i][self.indiceEpsilon][x]
                    if (self.ndfaMatrix[etat_pointe_epsilon][self.indiceEpsilon] != NULL):
                        for z in range(0, len(self.ndfaMatrix[etat_pointe_epsilon][self.indiceEpsilon])):
                            if ((self.ndfaMatrix[etat_pointe_epsilon][self.indiceEpsilon][z]) not in (self.ndfaMatrix[i][self.indiceEpsilon])):
                                self.ndfaMatrix[i][self.indiceEpsilon].append(self.ndfaMatrix[etat_pointe_epsilon][self.indiceEpsilon][z])
                tailleGroupe = len(lEtatsMemeGroupe)
                for j in range(0, self.nColonnes):
                    lEtatsCibles = []
                    for k in range(0, tailleGroupe):
                        if (lEtatsMemeGroupe[k] != NULL):
                            if (self.ndfaMatrix[lEtatsMemeGroupe[k]][j] != NULL):
                                for x in range(0, len(self.ndfaMatrix[lEtatsMemeGroupe[k]][j])):
                                    lEtatsCibles.append(self.ndfaMatrix[lEtatsMemeGroupe[k]][j][x])
                                    if (j < (self.nColonnes-3)):
                                        nonEtatPuit.add(self.ndfaMatrix[lEtatsMemeGroupe[k]][j][x])
                    if (self.ndfaMatrix[i][j] != NULL):
                        for x in range(0, len(self.ndfaMatrix[i][j])):
                            lEtatsCibles.append(self.ndfaMatrix[i][j][x])
                            if (j < (self.nColonnes-3)):
                                nonEtatPuit.add(self.ndfaMatrix[i][j][x])
                    if (len(lEtatsCibles) > 0):
                        self.nouveauNdfaMatrix[i][j] = lEtatsCibles
                    else:
                        self.nouveauNdfaMatrix[i][j] = NULL
                    self.nouveauNdfaMatrix[i][self.indiceEpsilon] = NULL
        for i in range(0, self.nLignes):
            listPleineDeNull = []
            if (not(i in nonEtatPuit)):
                self.nouveauNdfaMatrix[i] = listPleineDeNull


