import streamlit as st
import numpy as np
import pickle

linear_model = pickle.load(open("./model/model.sav", 'rb'))

day_lookup = {"Mon" : 0,"Tue" : 1,"Wed" : 2,"Thu" : 3,"Fri" : 4,"Sat" : 5,"Sun" :6}

st.header("Beach chair prediction")

st.write("""NOTICE: This is purely a demo. 
The data used for training the model was generated randomly,
so the results may not make any sense.""")

temp = st.slider("Max temp in C°", min_value=-10, max_value=50, value=15)
sun_min = st.slider("Sun minutes", min_value=0, max_value=1200, value=270)
wind = st.slider("Windspeed in km/h", min_value=0, max_value=63, value=25)
day = st.select_slider("Day of week", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], value="Fri")

day_of_week = day_lookup[day]

chairs_prediction = int(linear_model.predict(np.array([day_of_week, temp, sun_min, wind]).reshape(1, -1))[0])

# use max function to avoid negative number of beach chairs
chairs = max([chairs_prediction, 0])

st.subheader('Predicted number of chairs needed:')
st.header(chairs)

# remove streamlit menu for production
hide_streamlit_style = """ 
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)