"""
Exercice 9 Conversion binaire → décimal 
Écrire (et implémenter en python) un algorithme qui : 
1. lit un nombre binaire de 4 chiffres (ex : 1011) 
2. convertit en base 10 
3. affiche le résultat 
"""
# Demander à l'utilisateur d'entrer un nombre binaire de 4 chiffres
binaire = input("Entrez un nombre binaire de 4 chiffres : ")

# Initialiser une variable pour stocker le résultat décimal
decimal = 0
# Convertir le nombre binaire en décimal
for i in range(len(binaire)):
    # Convertir le caractère binaire en entier (0 ou 1) et calculer sa valeur décimale
    decimal += int(binaire[-(i + 1)]) * (2 ** i)

# Afficher le résultat décimal
print(f"Le nombre décimal correspondant est : {decimal}")