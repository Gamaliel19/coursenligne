"""
Exercice 7 Distance entre deux stations météo 
Écrire (et implémenter en python) un algorithme qui lit : 
1. A(x1, y1) 
2. B(x2, y2) 
Puis calcule : 
1. la distance AB
2. le milieu M de AB
"""

import math

# Demander à l'utilisateur d'entrer les coordonnées des stations météo A et B
x1 = float(input("Entrez la coordonnée x de la station A : "))
y1 = float(input("Entrez la coordonnée y de la station A : "))
x2 = float(input("Entrez la coordonnée x de la station B : "))
y2 = float(input("Entrez la coordonnée y de la station B : "))

# Calculer la distance AB
distance_ab = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
# Calculer le milieu M de AB
x_milieu = (x1 + x2) / 2
y_milieu = (y1 + y2) / 2

# Afficher les résultats
print(f"Distance AB : {distance_ab:.2f}")
print(f"Milieu M de AB : (x, y) = ({x_milieu:.2f}, {y_milieu:.2f})")


