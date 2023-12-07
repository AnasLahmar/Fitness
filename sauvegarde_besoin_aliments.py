import streamlit as st
import pandas as pd

def show_modal(new_champ, quantite_mesure, proteines, glucides, graisses, calories):
    # Créer un dictionnaire avec les données entrées
    nouvel_aliment = {
        "Aliments": new_champ,
        "Qte": quantite_mesure,
        "Protéine": proteines,
        "Carbs": glucides,
        "graisse": graisses,
        "besoin_calories": calories
    }

    # Charger les données existantes depuis le fichier Excel (s'il existe)
    try:
        df = pd.read_excel("besoin_en_aliments.xlsx")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Aliments", "Qte", "Protéine", "Carbs", "graisse", "besoin_calories"])

    # Créer un DataFrame à partir du dictionnaire de données
    new_data = pd.DataFrame([nouvel_aliment])

    # Ajouter les nouvelles données au DataFrame existant
    if not df.empty:
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data.copy()

    # Enregistrer la DataFrame mise à jour dans le fichier Excel
    df.to_excel("besoin_en_aliments.xlsx", index=False)