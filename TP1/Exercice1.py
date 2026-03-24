"""
Exercice 1  Température au carré 
Écrire (et implémenter en python) un algorithme qui demande une température (°C) à l’utilisateur, 
puis calcule et affiche son carré. 
"""

# Demander à l'utilisateur d'entrer une température en degrés Celsius
temperature_celsius = float(input("Entrez une température en degrés Celsius : "))

# Calculer le carré de la température
carre_temperature = temperature_celsius ** 2

# Afficher le résultat
print(f"Carré de la température en Celsius : {carre_temperature:.2f} °C²")
