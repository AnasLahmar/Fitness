import streamlit as st
import pandas as pd
def optimize_nutrition(delta_proteine,delta_carbs,delta_graisse,delta_calories):
    # Charger le fichier Excel dans un DataFrame
    besoin = pd.read_excel('data/besoin_en_aliments.xlsx')

    # Convert index values to strings
    macronutriments=st.radio('Macronutriments',["Protein","Carbs","Fat"],horizontal=True)
    if macronutriments == "Carbs":
        if delta_carbs>=0:
            st.success("Well done, you've eaten enough carbohydrates")
        else :
            delta_carbs = abs(delta_carbs)
            st.info("You still need to eat more Carbohydrates!")
            st.write(""" ### Here is a list of possible choices: """)

            qte_must_exist_in_aliment =10
            besoin_glucide = besoin[besoin["Carbs"]>=qte_must_exist_in_aliment]
            besoin_glucide = besoin[besoin["Carbs"] >= qte_must_exist_in_aliment].copy()  # Faites une copie explicite ici

            # Assuming besoin_glucide is a DataFrame
            besoin_glucide.loc[:, "Besoins en Glucides"] = (
                besoin_glucide["Qte"] * delta_carbs / besoin_glucide["Carbs"]
            ).round()

            # Displaying specific columns
            result = besoin_glucide[["Aliments", "Besoins en Glucides"]]
            st.write(result)



    elif macronutriments == "Protein":
        if delta_proteine>=0:
            st.success("Well done, you've eaten enough Proteins")
        else :
            delta_proteine = abs(delta_proteine)
            qte_must_exist_in_aliment = 5
            st.info("You still need to eat more Proteins!")
            st.write(""" ### Here is a list of possible choices: """)
            besoin_proteine = besoin[besoin["Protéine"]>=qte_must_exist_in_aliment]
            besoin_proteine = besoin[besoin["Protéine"] >= qte_must_exist_in_aliment].copy()  # Faites une copie explicite ici

            # Assuming besoin_glucide is a DataFrame
            besoin_proteine.loc[:, "Besoins en Glucides"] = (
                besoin_proteine["Qte"] * delta_proteine / besoin_proteine["Carbs"]
            ).round()

            # Displaying specific columns
            result = besoin_proteine[["Aliments", "Besoins en Glucides"]]
            st.write(result)


            
    elif macronutriments == "Fat":
        if delta_graisse>=0:
            st.success("Well done, you've eaten enough Fats")
        else :
            delta_graisse = abs(delta_graisse)
            qte_must_exist_in_aliment = 2
            st.info("You still need to eat more Fats!")
            st.write(""" ### Here is a list of possible choices: """)
            besoin_graisse = besoin[besoin["Protéine"]>=qte_must_exist_in_aliment]
            besoin_graisse = besoin[besoin["Protéine"] >= qte_must_exist_in_aliment].copy()  # Faites une copie explicite ici

            # Assuming besoin_glucide is a DataFrame
            besoin_graisse.loc[:, "Besoins en Glucides"] = (
                besoin_graisse["Qte"] * delta_graisse / besoin_graisse["Carbs"]
            ).round()

            # Displaying specific columns
            result = besoin_graisse[["Aliments", "Besoins en Glucides"]]
            st.write(result)

     
