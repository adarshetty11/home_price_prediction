import streamlit as st
import pydeck as pdk
import json
import pickle
import numpy as np

st.title('Home Price Prediction in Bengaluru🏠')

st.sidebar.title('Created By')
st.sidebar.markdown('[Adarsh Shetty](https://twitter.com/adarshetty11)')

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": 12.9716,
        "longitude": 77.5946,
        "zoom": 11,
        "pitch": 50,
    }))

st.subheader('Enter Details')

with open("columns.json","r") as f:
    columns = json.load(f)['data_columns']

location = st.selectbox('Select location',columns[3:])

area = st.number_input('Enter Area (Square ft.)',min_value=300,max_value=30000)

st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

bhk = st.radio('BHK',(1,2,3,4,5))

bath = st.radio('Bath',(1,2,3,4,5))

st.markdown('')

button = st.button('Predict Price')

with open("pickle_model","rb") as f:
    model = pickle.load(f)

if button:

    try:
        loc_index = columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(columns))
    x[0] = area
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    result = round(model.predict([x])[0],2)

    if result > 0:
        result_string = '₹'+str(result)+' lakhs'
        st.info(result_string)
    else:
        st.error('Please enter larger area , as house of this area is not available in this location')

