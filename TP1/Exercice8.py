"""
Exercice 8 Conversion décimal → binaire (capteur) 
Un capteur envoie des données en binaire. 
Écrire (et implémenter en python) un algorithme qui convertit un entier décimal (ex : humidité) en 
binaire en utilisant : 
1. DIV 
2. MOD 
"""

# Demander à l'utilisateur d'entrer un entier décimal
decimal = int(input("Entrez un entier décimal : "))

# Initialiser une chaîne pour stocker le résultat binaire
binaire = ""

# Convertir le nombre décimal en binaire en utilisant DIV et MOD
while decimal > 0:
    reste = decimal % 2  # Obtenir le reste (0 ou 1)
    binaire = str(reste) + binaire  # Ajouter le reste au début de la chaîne binaire
    decimal = decimal // 2  # Diviser le nombre par 2 pour la prochaine itération

# Afficher le résultat binaire
print(f"Le nombre binaire correspondant est : {binaire}")
