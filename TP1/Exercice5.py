"""
Exercice 5 Position d’un capteur mobile 
Un capteur météo se déplace selon : 
x(t) = a × t + b   
y(t) = c × t + d 
Écrire (et implémenter en python) un algorithme qui : 
1. lit a, b, c, d et t 
2. calcule la position (x, y) à l’instant t 
3. affiche le résultat 
"""

# Demander à l'utilisateur d'entrer les coefficients a, b, c, d et le temps t
a = float(input("Entrez le coefficient a : "))
b = float(input("Entrez le coefficient b : "))
c = float(input("Entrez le coefficient c : "))
d = float(input("Entrez le coefficient d : "))
t = float(input("Entrez le temps t : "))

# Calculer la position (x, y) à l'instant t
x = a * t + b
y = c * t + d

# Afficher le résultat
print(f"Position du capteur à l'instant t : (x, y) = ({x:.2f}, {y:.2f})")




