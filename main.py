#Import Library Needed.
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import pandas as pd
from ast import literal_eval

## Function Request Analyize Article for ALL Emiten.
def analyze_single_data(news : str):
    r = requests.post(f"http://127.0.0.1:8000/predict_single_data/?news_title={news}")
    return r

## Function Request Analyize Article for Spesific Emiten.
def analyze_data_collection(news : list):
    t = requests.post(f"http://127.0.0.1:8000/predict_data_collection/?news_title={news}")
    return t

def download_file():
    # Logic to generate or fetch the file to be downloaded
    file_content = "This is the content of the file."

    # Prepare the necessary headers for the download
    headers = {
        "Content-Disposition": f"attachment; filename=example.txt"
    }

    return file_content, headers

## Sidemenu / Sidebar
with st.sidebar:
    choose = option_menu("Predict", ["Single Data", "Data Collection"],
                         icons=['grid fill', 'search heart'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important"},
        "icon": {"color": "orange", "font-size": "20px"}, 
        "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

## Analyize Article for ALL Emiten.
if choose == "Single Data":
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">News Topic Classification</p>', unsafe_allow_html=True)    
    st.subheader("Indonesian Language News Topic Multiclassification")

    st.caption("Predict Single Data")
    with st.form(key='nlpForm'):
        news = st.text_area("Enter News Title Here", height=100)
        submit_button = st.form_submit_button(label='Analyze')
        
        # Button Analyize On-click :
        if submit_button:
            st.info("Results")
            # Predict Function
            predict = analyze_single_data(news)
            # Output Status Request
            st.write('Judul berita ini termasuk ke dalam topik: ', predict.text)

## Request Analyize Article for Spesific Emiten.
elif choose == "Data Collection":
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;}
        span[data-baseweb="tag"]{background-color: #95e85a !important;} 
        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">News Topic Classification</p>', unsafe_allow_html=True)    
    st.subheader("Indonesian Language News Topic Multiclassification")
    
    st.caption("Predict Data Collection")

    csv=None

    with st.form(key='nlpForm'):
        uploaded_file = st.file_uploader("Choose a CSV file")
        # news = st.text_area("Enter Article Here", height=200)
        submit_button = st.form_submit_button(label='Analyze')

        # Button Analyize On-click :
        if submit_button:
            st.info("Results")
            dataframe = pd.read_csv(uploaded_file)
            predict_label = analyze_data_collection(dataframe['title'].values)

            # Remove the opening and closing brackets and split the string by whitespace
            elements = predict_label.text[2:-2].split(",")

            # Convert the elements into a list
            array_predict_label = [element.replace("'","") for element in elements]

            dataframe['label']=array_predict_label
            dataframe['title'] = dataframe['title'].str.strip()
            csv = dataframe.to_csv().encode('utf-8')
            
            st.write(dataframe) 

    # try:
        # Check if the variable is defined
    if csv is not None:
            st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='labeld_data.csv',
            mime='text/csv',
        )  
    else:
            print("Data is not defined.")
         