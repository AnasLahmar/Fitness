import streamlit as st
import calendar
from metric_card import style_metric_cards
import numpy as np

def calculate_maintenance_calories(age, height, weight, gender, activity_level):
    if gender == "Man":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    if activity_level == "sedentary":
        maintenance_calories = bmr * 1.2
    elif activity_level == "Lightly active":
        maintenance_calories = bmr * 1.375
    elif activity_level == "Moderately active":
        maintenance_calories = bmr * 1.55
    elif activity_level == "Very active":
        maintenance_calories = bmr * 1.725
    else:
        maintenance_calories = bmr * 1.9

    return maintenance_calories

def calculate_calories(age, height, weight, gender, activity_level, target_weight_loss, target_period):
    maintenance_calories = calculate_maintenance_calories(age, height, weight, gender, activity_level)

    if target_period == "Week":
        days_in_period = 7
    elif target_period == "Month":
        days_in_month = calendar.monthrange(2023, 1)[1]  # Utilisation de janvier 2023 comme exemple
        weeks_in_month = days_in_month / 7
        days_in_period = weeks_in_month
    else:
        st.error("Unsupported period")
        return None, None

    deficit_calories = 500 * target_weight_loss * (days_in_period / 7)

    return maintenance_calories, max(0, maintenance_calories - deficit_calories)

def besoin_en_calories():
    # Interface Streamlit
    st.title("Aji te7sseb l'métabolisme")

    c1,c2,c3 = st.columns(3)

    # Entrées utilisateur
    age = c1.number_input("Age", min_value=1, max_value=150, value=23)
    height = c2.number_input("Height (cm)", min_value=1, max_value=300, value=179)
    weight = c3.number_input("Weight (kg)", min_value=1, max_value=500, value=76)
    
    """activity_levels_description = {
    "sedentary": "Little or no exercise.",
    "Lightly active": "About 10 to 20 minutes of light walking or jogging per day.",
    "Moderately active": "About 30 minutes of moderate exercise per day.",
    "Very active": "Intense training or prolonged exercise every day.",
    "Extremely active": "Intensive training, intense physical exercise, and daily physical work."
    }"""

    activity_levels_description = {
    "sedentary": "Little or no exercise.",
    "Lightly active": "Lightly active",
    "Moderately active": "Moderately active",
    "Very active": "Very active",
    "Extremely active": "Extremely active"
    }


    
    activity_level = c1.selectbox("Physical activity level", list(activity_levels_description.keys()), format_func=lambda x: activity_levels_description[x])    
    target_weight_loss = c2.number_input("Targeted weight loss (kg)", min_value=0.1, value=1.0)
    target_period = c3.selectbox("Period", ["Week", "Month"])
    gender = c2.radio("Gender", ["Male", "Female"],horizontal=True)

    # Calcul des calories
    result = calculate_calories(age, height, weight, gender, activity_level, target_weight_loss, target_period)

    # Affichage des résultats
    if result:
        maintenance_calories, deficit_calories = result
        st.subheader("Results in Metric Card")
        col1,col2=st.columns(2)
        col1.metric("Normal calories", np.round(maintenance_calories,2))
        col2.metric(f"Calories for losing {target_weight_loss} kg per {target_period.lower()}", np.round(deficit_calories,2))
        style_metric_cards()

    return weight,gender,activity_level