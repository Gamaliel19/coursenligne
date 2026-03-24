"""
Exercice 4  Coût d’irrigation 
Écrire (et implémenter en python) un algorithme qui lit : 
1. prix HT de l’eau (par unité) 
2. quantité utilisée 
3. taux de TVA 
Puis calcule et affiche le prix total TTC. 
Afficher clairement : 
1. Prix HT 
2. TVA 
3. Prix TTC 
"""

# Demander à l'utilisateur d'entrer le prix HT de l'eau, la quantité utilisée et le taux de TVA
prix_ht = float(input("Entrez le prix HT de l'eau (par unité) : "))
quantite = float(input("Entrez la quantité d'eau utilisée : "))
taux_tva = float(input("Entrez le taux de TVA (en %) : "))

# Calculer le prix total HT, la TVA et le prix TTC
prix_total_ht = prix_ht * quantite
tva = prix_total_ht * (taux_tva / 100)
prix_ttc = prix_total_ht + tva

# Afficher les résultats
print(f"Prix HT : {prix_total_ht:.2f} FCFA")
print(f"TVA : {tva:.2f} FCFA")
print(f"Prix TTC : {prix_ttc:.2f} FCFA")


