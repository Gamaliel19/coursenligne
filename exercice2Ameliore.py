import logging

# Configuration du logging
logging.basicConfig(
    filename="calcul_thermique.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def saisir_float(message):
    """Saisie sécurisée d'un float"""
    while True:
        try:
            valeur = float(input(message))
            return valeur
        except ValueError:
            print("❌ Entrée invalide. Veuillez saisir un nombre.")
            logging.warning("Entrée non numérique détectée")

def afficher_menu():
    print("\n" + "="*35)
    print("        MENU THERMIQUE")
    print("="*35)
    print("1. Indice thermique (T + H)")
    print("2. Différence thermique (T - H)")
    print("3. Produit thermique (T * H)")
    print("4. Rapport thermique (T / H)")
    print("0. Quitter")

def traiter_choix(choix, T, H):
    match choix:
        case 1:
            R = T + H
            print("👉 Indice thermique :", R)
            logging.info(f"Indice thermique calculé: {R}")

        case 2:
            R = T - H
            print("👉 Différence thermique :", R)
            logging.info(f"Différence thermique calculée: {R}")

        case 3:
            R = T * H
            print("👉 Produit thermique :", R)
            logging.info(f"Produit thermique calculé: {R}")

        case 4:
            if H != 0:
                R = T / H
                print("👉 Rapport thermique :", R)
                logging.info(f"Rapport thermique calculé: {R}")
            else:
                print("❌ Erreur : division par zéro")
                logging.error("Tentative de division par zéro")

        case 0:
            print("🔚 Fin du programme.")
            logging.info("Arrêt du programme par l'utilisateur")
            return False

        case _:
            print("❌ Choix invalide")
            logging.warning(f"Choix invalide: {choix}")

    return True


# 🔁 Boucle principale
while True:
    afficher_menu()

    try:
        choix = int(input("Votre choix : "))
    except ValueError:
        print("❌ Veuillez entrer un nombre valide.")
        logging.warning("Choix non numérique")
        continue

    if choix == 0:
        print("Au revoir 👋")
        break

    # Saisie des données uniquement si choix valide
    if choix in [1, 2, 3, 4]:
        T = saisir_float("Entrez la température (T) : ")
        H = saisir_float("Entrez l'humidité (H) : ")
        continuer = traiter_choix(choix, T, H)
        if not continuer:
            break