import streamlit as st
import pickle
import pandas as pd 
from datetime import datetime
import pickle
import os
from sauvegarde_besoin_aliments import show_modal

# Fonction pour sauvegarder les données dans un fichier Excel
def save_data(columns, data):
    data=[data]
    # Convert the data dictionary to a list of lists
    data_list = [[item[column] for column in columns] for item in data]
    

    # Create the DataFrame
    df = pd.DataFrame(data_list, columns=columns)

    # Convert 'Jour' column to datetime
    df['Jour'] = pd.to_datetime(df['Jour'])

    df.fillna(0, inplace=True)
    # Save to Excel
    df.to_excel("data/donnees_alimentaires.xlsx", index=False)

def add_to_excel(columns, data):
    # Charger le fichier Excel existant
    try:
        df = pd.read_excel('data/donnees_alimentaires.xlsx')
    except FileNotFoundError:
        # Si le fichier n'existe pas, créer un DataFrame vide
        df = pd.DataFrame(columns=columns)

    # Créer un DataFrame à partir du dictionnaire de données
    new_data = pd.DataFrame([data], columns=columns)

    # Ajouter les nouvelles données au DataFrame existant
    df = pd.concat([df, new_data], ignore_index=True)

    # Convertir la colonne 'Jour' en datetime
    df['Jour'] = pd.to_datetime(df['Jour'])
    df.fillna(0, inplace=True)
    # Écrire le DataFrame mis à jour dans le fichier Excel
    df.to_excel('data/donnees_alimentaires.xlsx', index=False)


    

def quantites_eated():
    m = st.markdown("""
            <style>
            div.stButton > button:first-child {
                background-color:#4B9DFF;
                color:#ffffff;
                width: 160px;
                height: 30px;
            }
            div.stButton > button:hover {
                background-color: #00ff00;
                color:#ff0000;
                }
            </style>""", unsafe_allow_html=True)
    # Charger les données existantes
    col1,col2 = st.columns(2)
    col1.title("Quantities consumed")


    # Charger les données existantes à partir du fichier pickle (s'il existe)
    try:
        with open("data/data_champs.pkl", "rb") as file:
            data_champs = pickle.load(file)
    except FileNotFoundError:
        # Si le fichier n'existe pas encore, initialisez avec les données actuelles
        data_champs = [{"Jour": datetime.today().strftime("%Y-%m-%d %H:%M:%S")}]

    c1, c2, c3, c4 = st.columns(4)
    list_column = [c1, c2, c3, c4]

  
    with st.sidebar.expander("Add a food") :
        new_champ = st.text_input("Enter the value")
        unite = st.selectbox("Unit", ['g', 'portion', 'litre'])
        quantite_mesure = st.number_input("Quantity of measurement")
        proteines = st.number_input("Proteins")
        glucides = st.number_input("Carbohydrates")
        graisses = st.number_input("Fats")
        calories = st.number_input("Calories")
        

        if st.button("Add"):
            show_modal(new_champ,quantite_mesure,proteines,glucides,graisses,calories)
            data_champs.append({new_champ: unite})

            # Sauvegarder les données mises à jour dans le fichier pickle
            with open("data/data_champs.pkl", "wb") as file:
                pickle.dump(data_champs, file)

    # Afficher tous les éléments de data_entries
    i = 0
    columns = ["Jour"]
    data = {"Jour": datetime.today().strftime("%Y-%m-%d %H:%M:%S")}
    for entry in data_champs[1:]:
        for key, value in entry.items():
            columns.append(key)
            if i == len(list_column):
                i = 0
            unique_key = f"{key}_{i}"  # Ajoutez un indice unique pour éviter les duplications
            columns.append(unique_key)
            widget_value = list_column[i].number_input(f"{key} ({value})", min_value=0, step=1, key=unique_key)
            entry_added = {unique_key: widget_value}
            data.update(entry_added)

            i += 1
    keys_list = list(data.keys())


    excel_file_path = "data/besoin_en_aliments.xlsx"

    # Check if the Excel file exists
    if os.path.isfile(excel_file_path):
        # File exists, read it into a DataFrame
        exist_besoin_data = pd.read_excel(excel_file_path)
        
        if len(exist_besoin_data) !=0 :
            # Bouton pour enregistrer les données
            if st.button("Save"):
                # Enregistrez les données comme vous le souhaitez (vous devrez définir la fonction save_data)
                exist_data = pd.read_excel("data/donnees_alimentaires.xlsx")
                if exist_data.empty:  # Correction ici, retirer les parenthèses
                    save_data(keys_list, data)
                    st.success("Data saved successfully!")
                else:
                    add_to_excel(keys_list, data)  # Correction ici, ajustement du message

                # Afficher les données existantes
                st.subheader("Information saved up to now")
                exist_data=pd.read_excel("data/donnees_alimentaires.xlsx")
                st.write(exist_data)
        
        else : 
            st.info("Please add and save a food item")
        
    else:
        # File doesn't exist, handle the case accordingly
        st.info("Please add and save a food item")

    