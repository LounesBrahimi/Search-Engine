from asyncio.windows_events import NULL
from SyntaxTree import SyntaxTree

class NDFA:
    
    # Indique à temps reel le numero d'un etat non existant et qu'on peut donc creer
    numeroEtat: int = 0

    CONCAT = 0xC04CA7
    ETOILE = 0xE7011E
    ALTERN = 0xA17E54
    PROTECTION = 0xBADDAD
    PARENTHESEOUVRANT = 0x16641664
    PARENTHESEFERMANT = 0x51515151
    DOT = 0xD07

    def __init__(self, nLignes: int):
        # Nombre de lignes de la matrice
        self.nLignes = nLignes
        # Nombre de colonnes de la matrice
        self.nColonnes = 259
        # La matrice representant l'automate finie non deterministe
        self.ndfaMatrix = [ [ 0 for i in range(self.nLignes) ] for j in range(self.nColonnes) ]
        # la colonne 256 indique si l'etat a des epslions transitions
        self.indiceEpsilon = 256
	    # la colonne 257 indique si l'etat est un etat initiale
        self.indiceInitiale = 257
	    # la colonne 257 indique si l'etat est un etat finale
        self.indiceFinale = 258

    """
    Constitue l'état initiale de l'automate selon l'arbre syntaxique, puis construit
	l'integralité de la matrice representant l'automate finie non deterministe avec 
	des epsilons transitions, la méthode peut notament appeler la méthode récursive "arbreToNDFARec"
	qui parcours tout l'arbre.
    """
    def arbreToNDFA(self, arbre: SyntaxTree):
        initiale: int = 0
        finale: int = 1
        nvEtat: int = finale + 1
        numeroEtat = nvEtat
        if( self.ndfaMatrix[initiale][self.indiceInitiale] == NULL ):
            list = []
            list.append(1)
            self.ndfaMatrix[initiale][self.indiceInitiale] = list
        else:
            self.ndfaMatrix[initiale][self.indiceInitiale].append(1)
        if( self.ndfaMatrix[finale][self.indiceFinale] == NULL ):
            list = []
            list.append(1)
            self.ndfaMatrix[finale][self.indiceFinale] = list
        else:
            self.ndfaMatrix[finale][self.indiceFinale].append(1)
        # ------------------------------------------------------------------
        # Dans le cas ou l'arbre est seulement une feuille, exemple (a) ou (b)
        if ((( ( (len(arbre.getSousArbre()) == 0) & (arbre.getRacine() != self.CONCAT) )
				& ((arbre.getRacine() != self.ETOILE) & (arbre.getRacine() != self.ALTERN)))
				& (arbre.getRacine() != self.DOT))):
                
            if (self.ndfaMatrix[initiale][arbre.getRacine()] == NULL):
                list = []
                list.append(nvEtat)
                self.ndfaMatrix[initiale][arbre.getRacine()] = list
            else:
                self.ndfaMatrix[initiale][arbre.getRacine].append(nvEtat)
            if (self.ndfaMatrix[nvEtat][self.indiceEpsilon] == NULL):
                list = []
                list.apped(finale)
                self.ndfaMatrix[nvEtat][self.indiceEpsilon] = list
            else:
                self.ndfaMatrix[nvEtat][self.indiceEpsilon].append(finale)
        #----------------------------------------------------------------------
        #Dans le cas d'une Alternation, exemple ( a | b ) 
        if ((len(arbre.getSousArbre()) > 1) & (arbre.getRacine() == self.ALTERN)):
            nvEtat2 = numeroEtat + 1
            numeroEtat = nvEtat2
            if (self.ndfaMatrix[initiale][self.indiceEpsilon] == NULL):
                list = []
                list.append(nvEtat)
                list.append(nvEtat2)
                self.ndfaMatrix[initiale][self.indiceEpsilon] = list
            else:
                self.ndfaMatrix[initiale][self.indiceEpsilon].append(nvEtat)
                self.ndfaMatrix[initiale][self.indiceEpsilon].append(nvEtat2)
            self.ndfaMatrix[initiale][self.indiceEpsilon].append(nvEtat)
            self.ndfaMatrix[initiale][self.indiceEpsilon].append(nvEtat2)
        #-------------------Fin Cas d'une alternation--------------------------
        # Dans le cas d'une concatenation, exemple : (a.b)
        if ((len(arbre.getSousArbre()) == 2) & ((arbre.getRacine() == self.CONCAT)
				| (arbre.getRacine() == self.DOT) ) ):
            
            if (len(arbre.getSousArbre()[0].getSousArbre()) == 0):
                #Si le fils gauche est une simple feuille
                if(self.ndfaMatrix[initiale][arbre.getSousArbre()[0].getRacine()] == NULL):
                    list =[]
                    list.append(nvEtat)
                    self.ndfaMatrix[initiale][arbre.getSousArbre()[0].getRacine()] = list
                    ancEtat = nvEtat
                    nvEtat = numeroEtat + 1
                    numeroEtat = nvEtat
                    if (self.ndfaMatrix[ancEtat][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(nvEtat)
                        self.ndfaMatrix[ancEtat][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[ancEtat][self.indiceEpsilon].append(nvEtat)
                else:
                    self.ndfaMatrix[initiale][arbre.getSousArbre()[0].getRacine()].append(nvEtat)
                    ancEtat = nvEtat
                    nvEtat = numeroEtat + 1
                    numeroEtat = nvEtat
                    self.ndfaMatrix[ancEtat][self.indiceEpsilon].append(nvEtat)
            else:
                # le cas ou le fils gauche n'est pas n'est pas une simple feuille :
                # 1) Si le fils gauche de la concaténation est une alternation :
                if ((len(arbre.getSousArbre()[0].getSousArbre()) > 1) & (arbre.getSousArbre()[0].getRacine() == self.ALTERN)):
                    if(self.ndfaMatrix[initiale][self.indiceEpsilon] == NULL):
                        list = []
                        list.append(nvEtat)
                        self.ndfaMatrix[initiale][self.indiceEpsilon] = list
                        etatAvConct = numeroEtat + 1
                        numeroEtat = etatAvConct
                        self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, initiale, etatAvConct)
                        nvEtat = etatAvConct
                    else:
                        self.ndfaMatrix[initiale][self.indiceEpsilon].append(nvEtat)
                        etatAvConct = numeroEtat + 1
                        numeroEtat = etatAvConct
                        self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, initiale, etatAvConct)
                        nvEtat = etatAvConct
                else:
                    # 2) Si le fils gauche de la concaténation est une concaténation : 
                    if ((len(arbre.getSousArbre()[0].getSousArbre()) > 1) & ((arbre.getSousArbre()[0].getRacine() == self.CONCAT)
							| (arbre.getSousArbre()[0].getRacine() == self.DOT))):
                        
                        if(self.ndfaMatrix[initiale][self.indiceEpsilon] == NULL):
                            list = []
                            list.append(nvEtat)
                            self.ndfaMatrix[initiale][self.indiceEpsilon] = list
                            etatAvConct = numeroEtat + 1
                            numeroEtat = etatAvConct
                            self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, initiale, etatAvConct)
                            nvEtat = etatAvConct
                        else:
                            self.ndfaMatrix[initiale][self.indiceEpsilon].append(nvEtat)
                            etatAvConct = numeroEtat + 1
                            numeroEtat = etatAvConct
                            self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, initiale, etatAvConct)
                            nvEtat = etatAvConct
                    elif ((len(arbre.getSousArbre()[0].getSousArbre()) == 1) & (arbre.getSousArbre()[0].getRacine() == self.ETOILE)):
                        # 3) Si le fils gauche de la concaténation est une étoile
                        if(self.ndfaMatrix[initiale][self.indiceEpsilon] == NULL):
                            list = []
                            list.append(nvEtat)
                            self.ndfaMatrix[initiale][self.indiceEpsilon] = list
                            etatAvConct = numeroEtat + 1
                            numeroEtat = etatAvConct
                            self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, initiale, etatAvConct)
                            nvEtat = etatAvConct
                        else:
                            self.ndfaMatrix[initiale][self.indiceEpsilon].append(nvEtat)
                            etatAvConct = numeroEtat + 1
                            numeroEtat = etatAvConct
                            self.arbreToNDFARec(arbre.sousArbre.getSousArbre()[0], nvEtat, initiale, etatAvConct)
                            nvEtat = etatAvConct
            
            #---------------Fin Cas Fils gauche d'une concaténation----------
            #----------------------------------------------------------------
            #Si le fils droit est une simple feuille
            if (len(arbre.getSousArbre()[1].getSousArbre()) == 0):
                ancEtat = nvEtat
                nvEtat = numeroEtat + 1
                numeroEtat = nvEtat
                if(self.ndfaMatrix[ancEtat][arbre.getSousArbre()[1].getRacine()] == NULL):
                    list = []
                    list.append(nvEtat)
                    self.ndfaMatrix[ancEtat][arbre.getSousArbre()[1].getRacine()] = list
                    if(self.ndfaMatrix[nvEtat][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(finale)
                        self.ndfaMatrix[nvEtat][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat][self.indiceEpsilon].append(finale)
                else:
                    self.ndfaMatrix[ancEtat][arbre.getSousArbre()[1].getRacine()].append(nvEtat)
                    if(self.ndfaMatrix[nvEtat][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(finale)
                        self.ndfaMatrix[nvEtat][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat][self.indiceEpsilon].append(finale)
            else:
                # Si le fils droit n'est pas une simple feuille
                self.arbreToNDFARec(arbre.getSousArbre()[1], nvEtat, initiale, finale)
        
        #------------------------ Fin Cas concaténation --------------------
        #dans le cas d'une boucle exemple : (a*)
        if ((len(arbre.getSousArbre()) == 1) & (arbre.getRacine() == self.ETOILE)):
            # si le sous arbre est une feuille simple exemple a :
            if (len(arbre.getSousArbre()[0].getSousArbre()) == 0):
                nvEtat2 = numeroEtat + 1
                numeroEtat = nvEtat2
                if (self.ndfaMatrix[initiale][self.indiceEpsilon] == NULL):
                    list = []
                    list.append(nvEtat)
                    list.append(nvEtat2)
                    self.ndfaMatrix[initiale][self.indiceEpsilon] = list
                    nvEtat3 = numeroEtat + 1
                    numeroEtat = nvEtat3
                    if (self.ndfaMatrix[nvEtat][arbre.getSousArbre()[0].getRacine()] == NULL):
                        list2 = []
                        list2.append(nvEtat3)
                        self.ndfaMatrix[nvEtat][arbre.getSousArbre()[0].getRacine()] = list2
                    else:
                        self.ndfaMatrix[nvEtat][arbre.getSousArbre()[0].getRacine()].append(nvEtat3)
                    if (self.ndfaMatrix[nvEtat3][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(nvEtat2)
                        list2.append(nvEtat)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat2)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat)
                    if(self.ndfaMatrix[nvEtat2][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(finale)
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon].append(finale)
                else:
                    self.ndfaMatrix[initiale][self.indiceEpsilon].append(nvEtat)
                    self.ndfaMatrix[initiale][self.indiceEpsilon].append(nvEtat2)
                    nvEtat3 = numeroEtat + 1
                    numeroEtat = nvEtat3
                    if (self.ndfaMatrix[nvEtat][arbre.getSousArbre()[0].getRacine()] == NULL):
                        list2 = []
                        list2.append(nvEtat3)
                        self.ndfaMatrix[nvEtat][arbre.getSousArbre()[0].getRacine()] = list2
                    else:
                        self.ndfaMatrix[nvEtat][arbre.getSousArbre()[0].getRacine()].append(nvEtat3)
                    if (self.ndfaMatrix[nvEtat3][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(nvEtat2)
                        list2.append(nvEtat)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat2)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat)
                    if(self.ndfaMatrix[nvEtat2][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(finale)
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon].append(finale)
            else:
                #si le sous arbre n'est pas une simple feuille exemple (a|b)* :
                nvEtat2 = numeroEtat + 1
                numeroEtat = nvEtat2
                if (self.ndfaMatrix[initiale][self.indiceEpsilon] == NULL):
                    list = []
                    list.append(nvEtat)
                    list.append(nvEtat2)
                    self.ndfaMatrix[initiale][self.indiceEpsilon] = list
                    nvEtat3 = numeroEtat + 1
                    numeroEtat = nvEtat3
					# sous arbre a bouclé--------------------------------------------------
                    self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, initiale, nvEtat3)
                    #----------------------------------------------------------------------
                    if (self.ndfaMatrix[nvEtat3][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(nvEtat2)
                        list2.append(nvEtat)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat2)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat)
                    if(self.ndfaMatrix[nvEtat2][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(finale)
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon].append(finale)
                else:
                    self.ndfaMatrix[initiale][self.indiceEpsilon].append(nvEtat)
                    self.ndfaMatrix[initiale][self.indiceEpsilon].append(nvEtat2)
                    nvEtat3 = numeroEtat + 1
                    numeroEtat = nvEtat3
					# sous arbre a bouclé--------------------------------------------------
                    self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, initiale, nvEtat3)
					#--------------------------------------------------------------------
                    if (self.ndfaMatrix[nvEtat3][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(nvEtat2)
                        list2.append(nvEtat)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat2)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat)
                    if(self.ndfaMatrix[nvEtat2][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(finale)
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon].append(finale)
    
    # Méthode qui transforme récursivement un arbre en un automate, elle est considéré
    # comme un complément de la méthode "arbreToNDFA" 
    def arbreToNDFARec(self, arbre: SyntaxTree, etatRacine: int , initiale: int, finale: int):
        nvEtat = self.numeroEtat + 1
        self.numeroEtat = nvEtat
		# Dans le cas ou l'arbre est une feuille simple exemple (a) ou (b)
        if ((((len(arbre.getSousArbre()) == 0) & (arbre.getRacine() != self.CONCAT))
			& ((arbre.getRacine() != self.ETOILE) & (arbre.getRacine() != self.ALTERN)))
			& (arbre.getRacine() != self.DOT)):

            if (self.ndfaMatrix[etatRacine][arbre.getRacine()] == NULL):
                list = []
                list.append(nvEtat)
                self.ndfaMatrix[etatRacine][arbre.getRacine()] = list
            else:
                self.ndfaMatrix[etatRacine][arbre.getRacine()].append(nvEtat)
            if (self.ndfaMatrix[nvEtat][self.indiceEpsilon] == NULL):
                list = []
                list.append(finale)
                self.ndfaMatrix[nvEtat][self.indiceEpsilon] = list
            else:
                self.ndfaMatrix[nvEtat][self.indiceEpsilon].append(finale)
        #----------------------- Fin cas simple --------------------
        # Dans le cas d'une Alternation, exemple ( a | b ) 
        if ((len(arbre.getSousArbre()) > 1) & (arbre.getRacine() == self.ALTERN)):
            nvEtat2 = self.numeroEtat + 1
            self.numeroEtat = nvEtat2
            if (self.ndfaMatrix[etatRacine][self.indiceEpsilon] == NULL):
                list = []
                list.append(nvEtat)
                list.append(nvEtat2)
                self.ndfaMatrix[etatRacine][self.indiceEpsilon] = list
            else:
                self.ndfaMatrix[etatRacine][self.indiceEpsilon].append(nvEtat)
                self.ndfaMatrix[etatRacine][self.indiceEpsilon].append(nvEtat2)
            self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, initiale, finale)
            self.arbreToNDFARec(arbre.getSousArbre()[1], nvEtat2, initiale, finale)
        #-------------------Fin Cas d'une alternation--------------------------
        # Dans le cas d'une concatenation, exemple : (a.b)
        if ((len(arbre.getSousArbre()) == 2) & ((arbre.getRacine() == self.CONCAT)
				| (arbre.getRacine() == self.DOT))):
            if (len(arbre.getSousArbre()[0].getSousArbre()) == 0):
                # Si le fils gauche est une simple feuille
                if(self.ndfaMatrix[etatRacine][arbre.getSousArbre()[0].getRacine()] == NULL):
                    list = []
                    list.append(nvEtat)
                    self.ndfaMatrix[etatRacine][arbre.getSousArbre()[0].getRacine()] = list
                    ancEtat = nvEtat
                    nvEtat = self.numeroEtat + 1
                    numeroEtat = nvEtat
                    if (self.ndfaMatrix[ancEtat][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(nvEtat)
                        self.ndfaMatrix[ancEtat][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[ancEtat][self.indiceEpsilon].add(nvEtat)
                else:
                    self.ndfaMatrix[etatRacine][arbre.getSousArbre()[0].getRacine()].append(nvEtat)
                    ancEtat = nvEtat
                    nvEtat = self.numeroEtat + 1
                    self.numeroEtat = nvEtat
                    self.ndfaMatrix[ancEtat][self.indiceEpsilon].append(nvEtat)
            else:
                # Si le fils gauche n'est pas une simple feuille :
                # 1) Si le fils gauche de la concaténation est une alternation :
                if ((len(arbre.getSousArbre()[0].getSousArbre()) > 1) 
                        & ((arbre.getSousArbre()[0]).getRacine() == self.ALTERN)):
                    if(self.ndfaMatrix[etatRacine][self.indiceEpsilon] == NULL):
                        list = []
                        list.append(nvEtat)
                        self.ndfaMatrix[etatRacine][self.indiceEpsilon] = list
                        etatAvConct = self.numeroEtat + 1
                        self.numeroEtat = etatAvConct
                        self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, initiale, etatAvConct)
                        nvEtat = etatAvConct
                    else:
                        self.ndfaMatrix[etatRacine][self.indiceEpsilon].append(nvEtat)
                        etatAvConct = self.numeroEtat + 1
                        self.numeroEtat = etatAvConct
                        self.arbreToNDFARec(arbre.getSousArbre[0], nvEtat, initiale, etatAvConct)
                        nvEtat = etatAvConct
                else:
                    # 2) Si le fils gauche de la concaténation est une concaténation :
                    if ((len(arbre.getSousArbre()[0].getSousArbre()) > 1) & ((arbre.getSousArbre()[0].getRacine() == self.CONCAT)
							| (arbre.getSousArbre()[0].getRacine() == self.DOT))):
                        if(self.ndfaMatrix[etatRacine][self.indiceEpsilon] == NULL):
                            list = []
                            list.append(nvEtat)
                            self.ndfaMatrix[etatRacine][self.indiceEpsilon] = list
                            etatAvConct = self.numeroEtat + 1
                            self.numeroEtat = etatAvConct
                            self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, initiale, etatAvConct)
                            nvEtat = etatAvConct
                        else:
                            self.ndfaMatrix[etatRacine][self.indiceEpsilon].append(nvEtat)
                            etatAvConct = self.numeroEtat + 1
                            self.numeroEtat = etatAvConct
                            self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, initiale, etatAvConct)
                            nvEtat = etatAvConct
                    else:
                        # 3) Si le fils gauche de la concaténation est une étoile :
                        if(self.ndfaMatrix[etatRacine][self.indiceEpsilon] == NULL):
                            list = []
                            list.append(nvEtat)
                            self.ndfaMatrix[etatRacine][self.indiceEpsilon] = list
                            etatAvConct = self.numeroEtat + 1
                            self.numeroEtat = etatAvConct
                            self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, initiale, etatAvConct)
                            nvEtat = etatAvConct
                        else:
                            self.ndfaMatrix[etatRacine][self.indiceEpsilon].append(nvEtat)
                            etatAvConct = self.numeroEtat + 1
                            self.numeroEtat = etatAvConct
                            self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, initiale, etatAvConct)
                            nvEtat = etatAvConct
            
            #Si le fils droit est une simple feuille
            if (len(arbre.getSousArbre()[1].getSousArbre()) == 0):
                ancEtat = nvEtat
                nvEtat = self.numeroEtat + 1
                self.numeroEtat = nvEtat
                if(self.ndfaMatrix[ancEtat][arbre.getSousArbre()[1].getRacine()] == NULL):
                    list = []
                    list.append(nvEtat)
                    self.ndfaMatrix[ancEtat][arbre.getSousArbre()[1].getRacine()] = list
                    if(self.ndfaMatrix[nvEtat][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(finale)
                        self.ndfaMatrix[nvEtat][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat][self.indiceEpsilon].append(finale)
                else:
                    self.ndfaMatrix[nvEtat][self.indiceEpsilon].append(finale)
                    if(self.ndfaMatrix[nvEtat][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(finale)
                        self.ndfaMatrix[nvEtat][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat][self.indiceEpsilon].append(finale)
            else:
                # Si le fils droit n'est pas une simple feuille
                self.arbreToNDFARec(arbre.getSousArbre()[1], nvEtat, initiale, finale)
        #---------------Fin Cas Fils gauche d'une concaténation----------
        #----------------------------------------------------------------
        # Dans le cas d'une boucle exemple : (a*)
        if ((len(arbre.getSousArbre()) == 1) & (arbre.getRacine() == self.ETOILE)):
            #si le sous arbre est une simple feuille, exemple a :
            if (len(arbre.getSousArbre()[0].getSousArbre()) == 0):
                nvEtat2 = self.numeroEtat + 1
                self.numeroEtat = nvEtat2
                if (self.ndfaMatrix[etatRacine][self.indiceEpsilon] == NULL):
                    list = []
                    list.append(nvEtat)
                    list.append(nvEtat2)
                    self.ndfaMatrix[etatRacine][self.indiceEpsilon] = list
                    nvEtat3 = self.numeroEtat + 1
                    self.numeroEtat = nvEtat3
                    if (self.ndfaMatrix[nvEtat][arbre.getSousArbre()[0].getRacine()] == NULL):
                        list2 = []
                        list2.append(nvEtat3)
                        self.ndfaMatrix[nvEtat][arbre.getSousArbre()[0].getRacine()] = list2
                    else:
                        self.ndfaMatrix[nvEtat][arbre.getSousArbre()[0].getRacine()].append(nvEtat3)
                    if (self.ndfaMatrix[nvEtat3][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(nvEtat2)
                        list2.append(nvEtat)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat2)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat)
                    if(self.ndfaMatrix[nvEtat2][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(finale)
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon].append(finale)
                else:
                    self.ndfaMatrix[etatRacine][self.indiceEpsilon].append(nvEtat)
                    self.ndfaMatrix[etatRacine][self.indiceEpsilon].append(nvEtat2)
                    nvEtat3 = self.numeroEtat + 1
                    self.numeroEtat = nvEtat3
                    if (self.ndfaMatrix[nvEtat][arbre.getSousArbre()[0].getRacine()] == NULL):
                        list2 = []
                        list2.append(nvEtat3)
                        self.ndfaMatrix[nvEtat][arbre.getSousArbre()[0].getRacine()] = list2
                    else:
                        self.ndfaMatrix[nvEtat][arbre.getSousArbre()[0].getRacine()].append(nvEtat3)
                    if (self.ndfaMatrix[nvEtat3][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(nvEtat2)
                        list2.append(nvEtat)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat2)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat)
                    if(self.ndfaMatrix[nvEtat2][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(finale)
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon].append(finale)
            else:
                # si le sous arbre n'est pas une simple feuille, exemple (a|b)* :
                nvEtat2 = self.numeroEtat + 1
                self.numeroEtat = nvEtat2
                if (self.ndfaMatrix[etatRacine][self.indiceEpsilon] == NULL):
                    list = []
                    list.append(nvEtat)
                    list.append(nvEtat2)
                    self.ndfaMatrix[etatRacine][self.indiceEpsilon] = list
                    nvEtat3 = self.numeroEtat + 1
                    self.numeroEtat = nvEtat3
					#sous arbre a bouclé--------------------------------------------------
                    self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, etatRacine, nvEtat3)
                    #--------------------------------------------------------------------
                    if (self.ndfaMatrix[nvEtat3][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(nvEtat2)
                        list2.append(nvEtat)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat2)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat)
                    if(self.ndfaMatrix[nvEtat2][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(finale)
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon].append(finale)
                else:
                    self.ndfaMatrix[etatRacine][self.indiceEpsilon].append(nvEtat)
                    self.ndfaMatrix[etatRacine][self.indiceEpsilon].append(nvEtat2)
                    nvEtat3 = self.numeroEtat + 1
                    self.numeroEtat = nvEtat3
                    # sous arbre a bouclé--------------------------------------------------
                    self.arbreToNDFARec(arbre.getSousArbre()[0], nvEtat, etatRacine, nvEtat3)
                    #--------------------------------------------------------------------
                    if (self.ndfaMatrix[nvEtat3][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(nvEtat2)
                        list2.append(nvEtat)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat2)
                        self.ndfaMatrix[nvEtat3][self.indiceEpsilon].append(nvEtat)
                    if(self.ndfaMatrix[nvEtat2][self.indiceEpsilon] == NULL):
                        list2 = []
                        list2.append(finale)
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon] = list2
                    else:
                        self.ndfaMatrix[nvEtat2][self.indiceEpsilon].append(finale)
    
    # Retourne la matrice representant l'automate finie non deterministe
    def getNdfaMatrix(self):
        return self.ndfaMatrix