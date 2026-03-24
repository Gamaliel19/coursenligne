"""
Exercice 3  Surface d’un champ 
Écrire (et implémenter en python) un algorithme qui lit : 
1. la longueur 
2. la largeur 
d’un champ agricole, puis calcule et affiche : 
1. le périmètre 
2. la surface 
"""

# Demander à l'utilisateur d'entrer la longueur et la largeur du champ
longueur = float(input("Entrez la longueur du champ (en mètres) : "))
largeur = float(input("Entrez la largeur du champ (en mètres) : "))

# Calculer le périmètre et la surface du champ
perimetre = 2 * (longueur + largeur)
surface = longueur * largeur

# Afficher les résultats
print(f"Périmètre du champ : {perimetre:.2f} mètres")
print(f"Surface du champ : {surface:.2f} mètres carrés")



