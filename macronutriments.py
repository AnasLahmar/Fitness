import streamlit as st


    


#def macronutriments(poids, besoin_calories, genre):

def macronutriments(weight, gender, activity_level):

    # Calculer les besoins nutritionnels en protéines, glucides et graisses

    st.success("Calculating Macronutrients Needs")
    goal = st.radio("Objectif", ["Reduce Weight", "Increase Muscle Mass", "Maintain Weight"], horizontal=True)

    # Définir les besoins en protéines de base en fonction du niveau d'activité
    protein_needs = {
        "sedentary": 1.0,
        "Lightly active": 1.2,
        "Moderately active": 1.4,
        "Very active": 1.6,
        "Extremely active": 2.0
    }

    # Calculer les besoins en protéines en fonction du poids et du genre
    if gender == "Male":
        protein_requirement = weight * protein_needs[activity_level] * 1.1  # Ajustement pour les hommes
    elif gender == "Female":
        protein_requirement = weight * protein_needs[activity_level]

    # Définir les ratios de macronutriments recommandés en fonction de l'objectif
    if goal == "Reduce Weight":
        carb_ratio = 0.4
        fat_ratio = 0.3
    elif goal == "Increase Muscle Mass":
        carb_ratio = 0.5
        fat_ratio = 0.3
    elif goal == "Maintain Weight":
        carb_ratio = 0.45
        fat_ratio = 0.35

    # Calculer les besoins en glucides et graisses en fonction des besoins en protéines
    carbohydrate_requirement = protein_requirement * carb_ratio
    fat_requirement = protein_requirement * fat_ratio
    st.info(f"Protein : {protein_requirement:.2f} g/day")
    st.info(f"Carbs : {carbohydrate_requirement:.2f} g/day")
    st.info(f"Fat : {fat_requirement:.2f} g/day")
    
    return protein_requirement, carbohydrate_requirement, fat_requirement

