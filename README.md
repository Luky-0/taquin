# Résolveur de taquin
Projet universitaire mettant en pratique la stratégie de recherche _A*_ pour
résoudre des taquins.
Développé en Python 3.6.0

## Installation

### Windows
- Télécharger le fichier `taquin.py`
- Si besoin, installer la dernière version de Python 3 sur 
[le site officiel](https://www.python.org/downloads/windows/)
- Lancer l'interpréteur : `Démarrer > Programmes > Python 3.6 > IDLE Python GUI`
- Indiquer à Python dans quel répertoire se trouve `taquin.py` :
```python
>>> import sys
>>> sys.path.append('C:\Users\utilisateur\Documents\dossierContenantTaquinPy') #exemple
```

### Linux
- Télécharger le fichier `taquin.py`
- Si besoin, installer la dernière version de Python 3 sur 
[le site officiel](https://www.python.org/downloads/windows/) ou avec votre 
gestionnaire de packages habituel
- Ouvrir un terminal, aller dans le répertoire contenant `taquin.py` et lancer
la commande `python`

## Utilisation

```python
>>> import taquin
>>> taquin.graph_search()
```
- On vous demandera la taille du taquin : le programme ne fonctionne pour l'instant
qu'avec des tailles entre 1 et 3 inclus.
- On demandera un coefficient qui détermine la façon de calculer la fonction 
d'évaluation servant à la résolution. Voir le code pour les détails.
- Le taquin s'affiche sous forme d'un ensemble de cases `(ligne,colonne) : numéro`
où le plus grand numéro représente le trou.
- La solution s'affiche sous forme d'une chaîne composée des lettres N, S, E et O,
représentant les mouvements du trou dans les directions Nord, Sud, Est et Ouest.
