"""
Exercice 2 Permutation de mesures 
Écrire (et implémenter en python) un algorithme qui demande deux mesures climatiques : 
1. x : température 
2. y : humidité 
Puis permute leurs valeurs et les affiche.
"""

x = float(input("Entrez la température : "))
y = float(input("Entrez l'humidité : "))

# Permutation des valeurs
x, y = y, x
print(f"Après permutation : Température = {x}, Humidité = {y}")
