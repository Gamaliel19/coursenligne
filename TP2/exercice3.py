T1,T2,T3=float(input("Entrez la première température: ")),float(input("Entrez la deuxième température: ")),float(input("Entrez la troisième température: "))

if T1 > T2 and T1 > T3:
    print("La première température est la plus élevée :", T1, "°C")
elif T2 > T3:
    print("La deuxième température est la plus élevée :", T2, "°C")
else:
    print("La troisième température est la plus élevée :", T3, "°C")


T = float(input("Entrez la température: "))

if 35 <= T < 50:
    print("Attention : risque de coup de chaleur")
elif 30 <= T < 35:
    print("Attention : risque de fatigue")
elif 25 <= T < 30:
    print("Attention : risque de déshydratation")
elif 20 <= T < 25:
    print("Attention : risque de crampes")
elif 15 <= T < 20:
    print("Attention : risque de malaise")
elif 10 <= T < 15:
    print("Attention : risque de frissons")
elif 5 <= T < 10:
    print("Attention : risque de gelures")
elif 0 <= T < 5:
    print("Attention : risque de gelures sévères")
elif T < 0:
    print("Attention : risque de gelures extrêmes")
else:
    print("Entrée invalide : la température doit être comprise entre 0 et 50 degrés Celsius")
    


