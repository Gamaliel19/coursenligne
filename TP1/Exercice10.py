"""
Exercice 10 Moyenne de mesures climatiques 
Écrire (et implémenter en python) un algorithme qui lit 4 températures et affiche : 
1. la somme 
2. la moyenne 
Deux méthodes : 
a) Avec 4 variables : T1, T2, T3, T4 
b) Avec une seule variable T (lecture successive) 
"""

# Méthode a) Avec 4 variables : T1, T2, T3, T4
T1 = float(input("Entrez la première température : "))
T2 = float(input("Entrez la deuxième température : "))
T3 = float(input("Entrez la troisième température : "))
T4 = float(input("Entrez la quatrième température : "))

# Calculer la somme et la moyenne
somme = T1 + T2 + T3 + T4
moyenne = somme / 4
# Afficher les résultats
print(f"Somme des températures : {somme:.2f}")
print(f"Moyenne des températures : {moyenne:.2f}")

# Méthode b) Avec une seule variable T (lecture successive)
somme = 0.0
for i in range(1, 5):
    T = float(input(f"Entrez la température {i} : "))
    somme += T
moyenne = somme / 4
print(f"Somme des températures : {somme:.2f}")
print(f"Moyenne des températures : {moyenne:.2f}")


"""
Algorithme Somme_Moyenne_Temperatures

Variables :
    T, somme, moyenne : Réels
    i : Entier

Début

    somme ← 0

    Pour i allant de 1 à 4 faire
        Écrire "Entrer la température ", i, " : "
        Lire T
        somme ← somme + T
    FinPour

    moyenne ← somme / 4

    Écrire "Somme = ", somme
    Écrire "Moyenne = ", moyenne

Fin

"""
