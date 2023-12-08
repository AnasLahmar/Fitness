import streamlit as st
from connexion import create_file, add_user, get_user_id, get_user_first_name
from streamlit_lottie import st_lottie
import json
# Interface Streamlit
def interface_connexion(user_id, first_name_connect):
    

    st.title("Hey ! : Aji T9aD Format")
    st.write(""" #### Application 100% Fitness and Nutrution""")
    st.write("devlopped by Anas LAHMAR")
    c1,c2=st.columns(2)
    with c2:
        lottie_coding = load_lottiefile("json/home.json")  # replace link to local lottie file
        st_lottie(
        lottie_coding,
        speed=1,
        reverse=False,
        loop=True,
        quality="low", # medium ; high

        height=400,
        width=None,)
    with c1 :
        # Formulaire de connexion
        with st.form("login_form"):
            st.write("Connexion")
            login_email = st.text_input("E-mail")
            login_password = st.text_input("Mot de passe", type="password")
            login_button = st.form_submit_button("Se connecter")

        # Initialisation de submit_button en dehors de la condition
        submit_button = None

        # Afficher le formulaire d'inscription si le lien est coché
        with st.expander("S'inscrire"):
            with st.form("signup_form"):
                st.write("Inscription")
                first_name = st.text_input("Prénom")
                last_name = st.text_input("Nom")
                email = st.text_input("E-mail")
                password = st.text_input("Mot de passe", type="password")
                submit_button = st.form_submit_button("S'inscrire")

        # Traitement du formulaire d'inscription
        if submit_button:
            add_user(first_name, last_name, email, password)

        # Traitement du formulaire de connexion
        if login_button:
            user_id = get_user_id(login_email)
            first_name_connect = get_user_first_name(user_id)

            if user_id:
                st.success(f"Connexion réussie! Bienvenue: {first_name_connect}")
                create_file(user_id)
            else:
                st.error("E-mail ou mot de passe incorrect. Si vous n'êtes pas encore inscrit, veuillez vous inscrire d'abord.")

        return user_id, first_name_connect





 # creer une animation
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

    