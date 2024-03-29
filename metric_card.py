import streamlit as st
def style_metric_cards(
    background_color: str = "#111930",#
    border_size_px: int = 1,
    border_color: str = "#CCC",
    border_radius_px: int = 5,
    border_left_color: str = "#06a206",
    box_shadow: bool = True,
):

    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                {box_shadow_str}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def style_metric_cards_vis(
    background_color: str = "#111930",
    border_size_px: int = 0.5,
    border_color: str = "#CCC",
    border_radius_px: int = 4,
    border_left_color: str = "#06a206",
    box_shadow: bool = True,
    font_size: str = "5px",  # Ajoutez cette ligne pour définir la taille de la police
):
    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.6rem 0 rgba(58, 59, 69, 0.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.3rem solid {border_left_color} !important;
                {box_shadow_str}
                font-size: {font_size} !important;  # Ajoutez cette ligne pour définir la taille de la police
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )