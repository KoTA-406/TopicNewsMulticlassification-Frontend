#Import Library Needed.
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import pandas as pd

## Function request predict news topic for single data.
def analyze_single_data(news : str):
    r = requests.post(f"http://127.0.0.1:8000/predict_single_data/?news_title={news}")
    return r

## Function request predict news topic for multiple data.
def analyze_data_collection(news : list):
    t = requests.post(f"http://127.0.0.1:8000/predict_data_collection/?news_title={news}")
    return t

## Function to download file 
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

## Title and Subtitle Section
st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
st.markdown('<p class="font">News Topic Classification</p>', unsafe_allow_html=True)    
st.subheader("Indonesian Language News Topic Multiclassification")

## UI for Predict single data
if choose == "Single Data":
    st.caption("Predict Single Data")
    with st.form(key='nlpForm'):
        news = st.text_area("Enter News Title Here", height=100)
        submit_button = st.form_submit_button(label='Submit')
        
        # Button Analyize On-click :
        if submit_button:
            st.info("Results")
            # Predict Function
            predict = analyze_single_data(news)
            # Output Status Request
            st.write('Judul berita ini termasuk ke dalam topik: ', predict.text)

## UI for Predict multiple data
elif choose == "Data Collection":
    st.caption("Predict Data Collection")

    csv=None

    with st.form(key='nlpForm'):
        uploaded_file = st.file_uploader("Choose a CSV file")
        submit_button = st.form_submit_button(label='Submit')

        # Button Analyize On-click :
        if submit_button:
            st.info("Results")
            # Read input file
            dataframe = pd.read_csv(uploaded_file)
            # Predict Function
            predict_label = analyze_data_collection(dataframe['title'].values)

            # Convert the elements into a list
            elements = predict_label.text[2:-2].split(",")
            array_predict_label = [element.replace("'","") for element in elements]

            # Show result
            dataframe['label']=array_predict_label
            dataframe['title'] = dataframe['title'].str.strip()

            # Write result to csv
            csv = dataframe.to_csv().encode('utf-8')
            st.write(dataframe) 

    # Section where the user can download the output
    if csv is not None:
            st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='labeld_data.csv',
            mime='text/csv',
        )  
    else:
            print("Data is not defined.")

# End of Line - main.py #