
    
T = float(input("Entrez la température(T) :"))
H = float(input("Entrez l'humidité(H) :"))

print("="*30)
print("\n Menu")
print("="*30)
print("1. Calcul de l'indice thermique")
print("2. Différence thermique")
print("3. Produit thermique")
print("4. Rapport thermique")

choix = int(input("Entrez votre choix (1/2/3) :"))

# Traitement avec match-case
match choix:
    case 1:
        print("Indice thermique :", T + H)
    case 2:
        print("Différence thermique :", T - H)
    case 3:
        print("Produit thermique :", T * H)
    case 4:
        if H != 0:
            print("Rapport thermique:", T / H)
        else:
            print("Erreur : division par zéro impossible")
    case _:
        print("Choix invalide")
