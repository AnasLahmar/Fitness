import streamlit as st
import pandas as pd
import json
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from visualisation import visualisation
from besoin_en_calories import besoin_en_calories
from quantites_eated import quantites_eated
from interface_connexion import interface_connexion


    



st.set_page_config(layout="wide")

# creer une animation
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# option menu
with st.sidebar:
    selected_option = option_menu(
    menu_title="Main Menu",
    options=["Home", "Caloric Needs", "Food Consumption", "Performance Data"],
    icons=["house", "bookmark-check-fill", "cart-dash", "bar-chart-line"],
    menu_icon="cast",  # optional
    default_index=0,
    orientation="vertical",
    styles={
        "nav-link-selected": {"background-color": "#4B9DFF"},
    }
    )



# Définir les variables de session
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if 'first_name' not in st.session_state:
    st.session_state.first_name = None



if selected_option == "Home":
    user_id_connect=None
    first_name_connect=None
    st.session_state.user_id, st.session_state.first_name = interface_connexion(user_id_connect, first_name_connect)




if selected_option == "Food Consumption":
    if st.session_state.user_id == None and st.session_state.first_name == None :
        st.info("Please connect !")


    else :
    
        quantites_eated(st.session_state.user_id)
        with st.sidebar : 
            lottie_coding = load_lottiefile("json/page.json")  # replace link to local lottie file
            st_lottie(
            lottie_coding,
            speed=1,
            reverse=False,
            loop=True,
            quality="low", # medium ; high

            height=160,
            width=None,)


# Définir les variables de session
if 'poids' not in st.session_state:
    st.session_state.poids = None

if 'genre' not in st.session_state:
    st.session_state.genre = None

if 'genre' not in st.session_state:
    st.session_state.activity_level = None



if selected_option == "Caloric Needs":
    if st.session_state.user_id == None and st.session_state.first_name == None :
        st.info("Please connect !")


    else :
        with st.sidebar :
            lottie_coding = load_lottiefile("json/page.json")  # replace link to local lottie file
            st_lottie(
            lottie_coding,
            speed=1,
            reverse=False,
            loop=True,
            quality="low", # medium ; high

            height=200,
            width=None,)

        poids, genre, activity_level = besoin_en_calories()
        
        # Mettre à jour les variables de session
        st.session_state.poids = poids
        st.session_state.genre = genre
        st.session_state.activity_level = activity_level

if selected_option == "Performance Data":
    if st.session_state.user_id == None and st.session_state.first_name == None :
        st.info("Please connect !")


    else :
        exist_data = pd.read_excel(f"data/donnees_alimentaires_{st.session_state.user_id}.xlsx")
        if len(exist_data) !=0 :
            if st.session_state.poids is None and st.session_state.genre is None and st.session_state.activity_level is None:
                st.warning("Tu dois sélectionner l'âge et ton poids avant d'entrer à cette partie")
            else:
                # Appel à votre fonction de visualisation
                visualisation(st.session_state.poids, st.session_state.genre, st.session_state.activity_level,st.session_state.user_id)
        else :
            st.info("Please Add your Fucking Food")
        with st.sidebar :
            lottie_coding = load_lottiefile("json/page.json")  # replace link to local lottie file
            st_lottie(
            lottie_coding,
            speed=1,
            reverse=False,
            loop=True,
            quality="low", # medium ; high

            height=200,
            width=None,)