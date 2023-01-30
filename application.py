import streamlit as st
import json
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import pandas as pd 


#==============================================Start=============================================================
# Interface Application------------------------------------------------------------------------------------------
st.write(""" ## Projet Génie Industriel et Productif :""")
st.write(""" ###  Automatiser le processus d'affectation des palettes """)

selected=option_menu(
    menu_title="Main Menu",
    options=["Home","Data Overview","Palette Optimales"],
    icons=["house","bar-chart"],
    menu_icon="cast",  # optional
    default_index=0,
    orientation="horizontal",  
    styles={
        "nav-link-selected": {"background-color": "#4B9DFF"},
    } 

     )
   

#========================================================Accueil===========================================
if selected=="Home":
    # creer une animation
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)
    lottie_coding = load_lottiefile("pc.json")  # replace link to local lottie file
    st_lottie(
    lottie_coding,
    speed=1,
    reverse=False,
    loop=True,
    quality="low", # medium ; high

    height=300,
    width=None,
    key=None,
)
#======================================================Data Overview=======================================
if selected=="Data Overview":
    with st.sidebar:
    # creer une animation
    # Creer un slider
        def load_lottiefile(filepath: str):
                with open(filepath, "r") as f:
                    return json.load(f)
        lottie_coding = load_lottiefile("lottie2.json")  # replace link to local lottie file
        st_lottie(lottie_coding,speed=1,reverse=False,loop=True,quality="high",height=200, width=None, key=None,)
    # Chose csv file------------------------------------------------------------------------------------------
    st.sidebar.title("Select Your Dataset")
    upload_file=st.sidebar.file_uploader("Select:",type=["csv"])
    if upload_file is not None:
        data=pd.read_csv(upload_file)
        st.success("Dataset has selected successfully")
         ##### Encodding------------------------------------------------------------------------------------------
        if st.checkbox("Discover your Data") :
            st.write(""" ## Discover your Data :""")
            radiodicover=st.radio("",("Header","Shape","Description","Missing Value"))
            if radiodicover=="Header":
                st.write(""" ### Results : """)
                st.write(data.head(data.shape[0]))
            if radiodicover=="Shape":
                st.write(""" ### Results : """)
                st.success(data.shape)
            if radiodicover=="Description":
                st.write(""" ### Results : """)
                st.write(data.describe())
            if radiodicover=="Missing Value":
                st.write(""" ### Results : """)
                st.write(data.isnull().sum())

    else:
        st.info("Select your Dataset")
#==============================================Clustering=======================================================
if selected=="Palette Optimales":
    with st.sidebar:
    # creer une animation
    # Creer un slider
        def load_lottiefile(filepath: str):
                with open(filepath, "r") as f:
                    return json.load(f)
        lottie_coding = load_lottiefile("lottie2.json")  # replace link to local lottie file
        st_lottie(lottie_coding,speed=1,reverse=False,loop=True,quality="high",height=200, width=None, key=None,)

        df2 = pd.read_csv('data2new.csv')
        #df2.to_csv('data2new.csv', index=False)
        #df2 = pd.read_csv('data2new.csv')

        # Constraint
        st.sidebar.title("Constraint")
        pallet =st.sidebar.slider("Maximum Height of palette : ",0, 5, 1)
        poids =st.sidebar.slider("Maximum Weight of palette : ", 0, 60, 23)
        #input
        pallet*=100   # pallette en cm
        poids*=100  # poids en Kg

    st.write(''' ### Material : ''')
    material=st.selectbox('Select a Material',df2["material"])
    if material:
        st.info("You have selected {}".format(material))
    else:
        st.info("Select Matreial wanted !")
    row_index2 = df2.index[df2['material'] == material].tolist()[0]
    number_package=st.number_input("number of package", min_value=1, value=3)

    # Hauteur
    number=1
    while(df2['Height'][row_index2]*number_package>pallet):
        number+=1
        pallet=pallet*number

    # Poids
    newpoids=poids*number
    while(df2['Gross weight packaging unit(g)'][row_index2]*number_package>newpoids):
        number+=1
        newpoids=poids*number

    if st.checkbox("Show the Results"):
        st.success("To delivre the Material {} with {} package(s) you need {} palette(s)".format(material,number_package,number))
        
    

