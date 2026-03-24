"""
Exercice 6 Conversion du temps climatique 
Écrire (et implémenter en python) un algorithme qui lit une durée en secondes (durée d’observation 
météo) et affiche : 
1. heures 
2. minutes 
3. secondes 
Exemple : 
3800 s → 1 h 3 min 20 s 
"""

# Demander à l'utilisateur d'entrer une durée en secondes
duree_secondes = int(input("Entrez une durée en secondes : "))

# Calculer les heures, les minutes et les secondes
heures = duree_secondes // 3600
minutes = (duree_secondes % 3600) // 60
secondes = duree_secondes % 60

# Afficher le résultat
print(f"{duree_secondes} s → {heures} h {minutes} min {secondes} s")


