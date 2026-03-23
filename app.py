import streamlit as st
from streamlit_ace import st_ace

st.set_page_config(page_title="Cours Python Interactif", layout="centered")

st.title("🐍 Introduction à l'Algorithmique & Python")

# --- SIDEBAR NAVIGATION ---
page = st.sidebar.radio("Navigation", ["Accueil", "Module 1: Variables", "Module 2: Boucles", "Quiz Final"])

if page == "Accueil":
    st.header("Bienvenue !")
    st.write("Ce cours vous apprendra les bases de la programmation de manière interactive.")
    st.info("Utilisez le menu à gauche pour commencer.")

elif page == "Module 1: Variables":
    st.header("Les Variables")
    st.write("Une variable est comme une boîte dans laquelle on stocke une information.")
    
    st.code("nom = 'Alice'\nage = 25", language="python")
    
    st.subheader("💻 À vous de jouer !")
    st.write("Créez une variable `score` égale à 100 et affichez-la.")
    
    # Zone de code interactive
    code = st_ace(language="python", theme="monokai", height=150)
    
    if st.button("Vérifier mon code"):
        try:
            exec(code)
            if "score" in locals() and score == 100:
                st.success("Bravo ! C'est correct.")
            else:
                st.warning("Presque ! Assurez-vous d'avoir nommé la variable 'score'.")
        except Exception as e:
            st.error(f"Erreur : {e}")

elif page == "Quiz Final":
    st.header("Testez vos connaissances")
    q1 = st.radio("Quelle fonction permet d'afficher un message ?", ["read()", "print()", "show()"])
    
    if st.button("Soumettre"):
        if q1 == "print()":
            st.success("Correct !")
        else:
            st.error("Essaye encore !")