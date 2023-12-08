import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from optimization import optimize_nutrition

from metric_card import style_metric_cards_vis
from macronutriments import macronutriments

def visualisation(poids, genre,activity_level,user_id):
    m = st.markdown("""
            <style>
            div.stButton > button:first-child {
                background-color:#4B9DFF;
                color:#ffffff;
                width: 210px;
                height: 50px;
            }
            div.stButton > button:hover {
                background-color: #00ff00;
                color:#ff0000;
                }
            </style>""", unsafe_allow_html=True)
    with st.sidebar:
        besoin_calories = st.number_input("besoin_calories (kal)", min_value=0, value=1500, step=1)
        proteines, glucides, graisses = macronutriments(poids, genre, activity_level)

    # Charger le fichier excel dans un DataFrame
    besoin = pd.read_excel(f'data/besoin_en_aliments_{user_id}.xlsx')

    aliment_jour = pd.read_excel(f'data/donnees_alimentaires_{user_id}.xlsx', parse_dates=['Jour'])
    columns_list_aliments = aliment_jour.columns[1:].tolist()

    # Sélectionner les colonnes d'intérêt
    selected_columns = besoin.iloc[:, 2:]

    # Diviser les valeurs par la colonne "Qte"
    result = selected_columns.div(besoin["Qte"], axis=0)
    selected_columns_result = result[["Protéine", "Carbs", "graisse", "besoin_calories"]]

    # Préparation des aliments
    sum_per_column_per_day = aliment_jour.groupby(aliment_jour['Jour'].dt.date)[columns_list_aliments].sum()

    # Effectuer la multiplication matricielle
    result_matrix = np.dot(sum_per_column_per_day[columns_list_aliments].values, selected_columns_result.values)

    # Créer un DataFrame à partir du résultat
    result_df = pd.DataFrame(result_matrix, columns=["Protein", "Carbs", "Fat", "Calories"]) 

    # Index pour suivre la ligne actuelle
    if 'index' not in st.session_state:
        st.session_state.index = 0

    # Fonction pour mettre à jour l'index
    def update_index(direction):
        if direction == 'next' and st.session_state.index < len(result_df) - 1:
            st.session_state.index += 1
        elif direction == 'previous' and st.session_state.index > 0:
            st.session_state.index -= 1

    # Ajouter la colonne 'Jour' au DataFrame résultant en premier
    result_df.insert(0, 'Jour', sum_per_column_per_day.index)

    c1,c2,c3=st.columns(3)

    if c1.button('Previous'):
        update_index('previous')
    if c2.button('Next'):
        update_index('next')
    c3.warning(f"Date : {result_df['Jour'][st.session_state.index]}")

    # Afficher les boutons de navigation
    col1, col2, col3, col4 = st.columns(4)
    # DEFICIT POUR CHAQUE MACRONITRIMENTS
    delta_proteine = round(result_df['Protein'].iloc[st.session_state.index] - proteines, 2)
    delta_carbs = round(result_df['Carbs'].iloc[st.session_state.index] - glucides, 2)
    delta_graisse = round(result_df['Fat'].iloc[st.session_state.index] - graisses, 2)
    delta_calories = round(result_df['Calories'].iloc[st.session_state.index] - besoin_calories, 2)


    # Afficher les cartes métriques pour la dernière ligne par défaut
    last_index = len(result_df) - 1
    col1.metric("Protein (g)", value=f"{round(result_df['Protein'].iloc[last_index], 2)} ",
                delta=f"{delta_proteine} g")
    col2.metric("Carbs (g)", value=f"{round(result_df['Carbs'].iloc[last_index], 2)}",
                delta=f"{delta_carbs} g")
    col3.metric("Fat (g)", value=f"{round(result_df['Fat'].iloc[last_index], 2)}",
                delta=f"{delta_graisse} g")
    col4.metric("Calories (kcal)", value=f"{round(result_df['Calories'].iloc[last_index], 2)}",
                delta=f"{delta_calories} kcal")

    style_metric_cards_vis()
    
   

    # Créer un graphique avec Plotly
    fig = px.line(result_df, x='Jour', y=["Protein", "Carbs", "Fat", "Calories"],
                  labels={'value': 'Quantité', 'variable': 'Nutrients'},
                  title='Variation of nutrients per day')
    

    # Ajuster la taille de la figure
    fig.update_layout(
        width=1700,  # Définir la largeur de la figure
        height=400,  # Définir la hauteur de la figure
    )

    # Afficher le graphique avec Plotly
    st.plotly_chart(fig)

    if st.checkbox("Optimize nutrition"):
        # Appeler la fonction d'optimisation
        optimize_nutrition(delta_proteine,delta_carbs,delta_graisse,delta_calories,user_id)


