"""
Le but du projet est de réaliser un résolveur de taquin utilisant A*.
On crée un taquin résoluble, on fait tourner A* dessus avec différentes 
heuristiques, et on compare les résultats.

"""
import math
import copy
from random import randint
###############################################################################
# CONSTANTES                                                                  #
###############################################################################

POIDS = ((36, 12, 12, 4, 1, 1, 4, 1, 0),    #pi1
        (8, 7, 6, 5, 4, 3, 2, 1, 0),        #pi2 = pi3
        (8, 7, 6, 5, 4, 3, 2, 1, 0),        #pi3 = pi2
        (8, 7, 6, 5, 3, 2, 4, 1, 0),        #pi4 = pi5
        (8, 7, 6, 5, 3, 2, 4, 1, 0),        #pi5 = pi4
        (1, 1, 1, 1, 1, 1, 1, 1, 0))        #pi6

COEFF = (4, 1, 4, 1, 4, 1)  #rho1 à rho6

###############################################################################
# CLASSES ET METHODES
###############################################################################

class Taquin:
    """Liste des attributs
    
    taille : au moins 3

    etat : représentation matricielle par des couples ((abs,ord), valeur)
    Le trou est codé par la valeur maximale (taille*taille - 1)

    chemin : liste des mouvements du trou pour parvenir á l'état courant.
    N, S, E, O représentent respectivement Nord, Sud, Est, Ouest.
    Exemples de chemins : 'OSSOSNEEN', 'E', '' (chaîne vide pr état initial)

    cout : cout du chemin actuel. Correspond au nombre de déplacements 

    f : fonction d'évaluation pour A*. f = cout + distanceManhattan
    """

    def __init__(self, n):
        self.taille = n
        self.etat = {(j//n, j%n): j for j in range(n*n)}
        self.chemin = ""
        self.cout = 0
        self.f = 0

    def est_resoluble(self):
        pass

    def est_solution(self):
        """Renvoie True si le taquin est résolu."""
        return self.etat == Taquin(self.taille).etat

    def chercher(self, e):
        """Retourne les coordonnées de la case e"""
        for i in range(self.taille):
            for j in range(self.taille):
                if self.etat[(i,j)] == e:
                    return (i,j)

    def bouger_trou(self, sens):
        """Déplace le trou dans l'une des directions Nord, Sud, Est, Ouest,
        et renvoie le taquin résultant avec le chemin et le cout mis à jour."""
        copie_T = copy.deepcopy(self)
        trou = self.chercher(len(self.etat) - 1)
        if sens == "N":
            copie_T.etat[trou] = self.etat[(trou[0]-1, trou[1])]
            copie_T.etat[(trou[0]-1, trou[1])] = self.etat[trou]
            copie_T.chemin += "N"
        elif sens == "S":
            copie_T.etat[trou] = self.etat[(trou[0]+1, trou[1])]
            copie_T.etat[(trou[0]+1, trou[1])] = self.etat[trou]
            copie_T.chemin += "S"
        elif sens == "E":
            copie_T.etat[trou] = self.etat[(trou[0], trou[1]+1)]
            copie_T.etat[(trou[0], trou[1]+1)] = self.etat[trou]
            copie_T.chemin += "E"
        elif sens == "O":
            copie_T.etat[trou] = self.etat[(trou[0], trou[1]-1)]
            copie_T.etat[(trou[0], trou[1]-1)] = self.etat[trou]
            copie_T.chemin += "O"
        else:
            print("Mouvement non reconnu. Devrait être N, S, E ou O.")
            print("Ça n'est pas censé se produire.")

        copie_T.cout += 1
        return copie_T

    def preparer_taquin(self):
        """Prend un taquin résolu et le mélange avec un grand nombre de 
        mouvements aléatoires. On est sûr qu'il est résolvable en faisant ça."""
        trou = list(self.chercher(len(self.etat)-1))

        trouHaut = (trou[1] == 0)
        trouBas = (trou[1] == self.taille - 1)
        trouGauche = (trou[0] == 0)
        trouDroite = (trou[0] == self.taille - 1)
        trouHG = trouHaut and trouGauche
        trouHD = trouHaut and trouDroite
        trouBG = trouBas and trouGauche
        trouBD = trouBas and trouDroite

        for i in range(100):
            x = randint(1,12)
            if trouHG:
                if x <= 6:
                    self = self.bouger_trou("E")
                    trou[1] += 1
                else:
                    self = self.bouger_trou("S")
                    trou[0] += 1
            elif trouHD:
                if x <= 6:
                    self = self.bouger_trou("O")
                    trou[1] -= 1
                else:
                    self = self.bouger_trou("S")
                    trou[0] += 1
            elif trouBG:
                if x <= 6:
                    self = self.bouger_trou("E")
                    trou[1] += 1
                else:
                    self = self.bouger_trou("N")
                    trou[0] -= 1
            elif trouBD:
                if x <= 6:
                    self = self.bouger_trou("O")
                    trou[1] -= 1
                else:
                    self = self.bouger_trou("N")
                    trou[0] -= 1
            elif trouHaut:
                if x <= 4:
                    self = self.bouger_trou("O")
                    trou[1] -= 1
                elif 4 < x <= 8:
                    self = self.bouger_trou("S")
                    trou[0] += 1
                else:
                    self = self.bouger_trou("E")
                    trou[1] += 1
            elif trouBas:
                if x <= 4:
                    self = self.bouger_trou("O")
                    trou[1] -= 1
                elif 4 < x <= 8:
                    self = self.bouger_trou("N")
                    trou[0] -= 1
                else:
                    self = self.bouger_trou("E")
                    trou[1] += 1
            elif trouGauche:
                if x <= 4:
                    self = self.bouger_trou("N")
                    trou[0] -= 1
                elif 4 < x <= 8:
                    self = self.bouger_trou("E")
                    trou[1] += 1
                else:
                    self = self.bouger_trou("S")
                    trou[0] += 1
            elif trouDroite:
                if x <= 4:
                    self = self.bouger_trou("N")
                    trou[0] -= 1
                elif 4 < x <= 8:
                    self = self.bouger_trou("O")
                    trou[1] -= 1
                else:
                    self = self.bouger_trou("S")
                    trou[0] += 1
            else:
                if x <= 3:
                    self = self.bouger_trou("N")
                    trou[0] -= 1
                elif 3 < x <= 6:
                    self = self.bouger_trou("E")
                    trou[1] += 1
                elif 6 < x <= 9:
                    self = self.bouger_trou("S")
                    trou[0] += 1
                else:
                    self = self.bouger_trou("O")
                    trou[1] -= 1

            return self


    def expanser(self):
        """Renvoie une liste des états accessibles à partir de l'état actuel."""

        trou = self.chercher(len(self.etat) - 1)
        
        trouHaut = (trou[1] == 0)
        trouBas = (trou[1] == self.taille - 1)
        trouGauche = (trou[0] == 0)
        trouDroite = (trou[0] == self.taille - 1)
        trouHG = trouHaut and trouGauche
        trouHD = trouHaut and trouDroite
        trouBG = trouBas and trouGauche
        trouBD = trouBas and trouDroite

        eNord,eSud,eOuest,eEst = None,None,None,None

        if trouHG:
            eEst = e.bouger_trou("E")
            eSud = e.bouger_trou("S")
        elif trouHD:
            eOuest = e.bouger_trou("O")
            eSud = e.bouger_trou("S")
        elif trouBG:
            eNord = e.bouger_trou("N")
            eEst = e.bouger_trou("E")
        elif trouBD:
            eNord = e.bouger_trou("N")
            eOuest = bouger_trou("O")
        elif trouHaut:
            eEst = e.bouger_trou("E")
            eSud = e.bouger_trou("S")
            eOuest = e.bouger_trou("O")
        elif trouBas:
            eNord = e.bouger_trou("N")
            eEst = e.bouger_trou("E")
            eOuest = e.bouger_trou("O")
        elif trouGauche:
            eNord = e.bouger_trou("N")
            eSud = e.bouger_trou("S")
            eEst = e.bouger_trou("E")
        elif trouDroite:
            eNord = e.bouger_trou("N")
            eSud = e.bouger_trou("S")
            eOuest = bouger_trou("O")
        else:
            eNord = e.bouger_trou("N")
            eSud = e.bouger_trou("S")
            eEst = e.bouger_trou("E")
            eOuest = bouger_trou("O")

        return [eNord,eSud,eOuest,eEst]

    def dist_elem(self, e):
        """Renvoie le nombre de cases séparant l'élément e de sa position 
        voulue. Fonction intermédiaire pour la distance de Manhattan."""

        d = 0
        position_actuelle = self.chercher(e)
        position_voulue = (e // self.taille, e % self.taille)
        d = abs(position_actuelle[0] - position_voulue[0]) \
                + abs(position_actuelle[1] - position_voulue[1])
        return d

    def manhattan(self, k):
        """Calcule la distance Manhattan avec POIDS[k] et COEFF[k].
        Fonction intermédiaire pour la fonction d'évaluation f."""
        elem = [self.dist_elem(i) for i in range(len(self.etat))]
        elem = tuple(elem) 
        return sum(POIDS[k][i] * elem(i) for i in range(9)) / COEFF[k]

    def calculer_f(self, k):
        self.f = self.cout + self.manhattan(k)


class Frontiere:
    """Liste d'états triés selon leur valeur de f (ordre croissant)."""
    def __init__(self):
        etats = []

    def ajouter(self, e):
        """Ajoute e à la bonne position en fonction de sa valeur de f."""
        if self.etats == []:
            self.etats.insert(0,e)
        else:
            fait = False
            for i in range(len(self.etats)):
                if self.etats[i].f >= e.f:
                    self.etats.insert(i,e)
                    fait = True
            if not fait:
                self.etats.insert(len(self.etats),e)


class DejaExplores:
    """Arbre binaire contenant les états déjà explorés"""
    def __init__(self):
        pass

    def ajouter(self, e):
        pass

###############################################################################
# ALGORITHME A*                                                               #
###############################################################################

def a_etoile():
    # Initialisation =====================================================
    t0 = Taquin(input("Entrer la taille du taquin : "))
    pond = input("Pondération pour les distances de Manhattan (0 à 5) : ")

    t0.melanger_taquin() #pour avoir un taquin non résolu
    print(t0.etat) #affiche le taquin initial
    frontiere = Frontiere()
    frontiere.ajouter(t0)
    historique = DejaExplores() #crée l'ensemble des états déjà explorés

    if not t0.est_resoluble():
        return "Taquin non résoluble : pas de solution"
    if t0.est_solution():
        print("Le taquin est déjà solution.")
        return ""

    # Boucle principale =================================================
    while True:

        if len(frontiere.etats) == 0:
            return "Frontière vide : pas de solution"

        t = frontiere.etats.pop(0)
        if t.est_solution():
            return t.chemin

        trou = t.chercher(len(t.etats)-1)
        expansion = t.expanser(trou) #On récupère une liste des états accessibles
        historique.ajouter(t)
        for i in range(len(expansion)):
            if not expansion[i] == None:
                expansion[i].f = expansion[i].calculer_f(cout, pond)
                if not historique.contient(expansion[i]):
                    frontiere.ajouter(expansion[i])

