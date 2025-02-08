import streamlit as st 
from yelpreview.utils.config import Config
from yelpreview.configs.config import CFGLog
from yelpreview.executor.inferrer import Inferrer

config = Config.from_json(CFGLog)
model_name = config.output.model_name

st.title("Yelp Review Rating Prediction")
input_document = st.text_area(label='Input your text review')
inferrer = Inferrer()

# .infer still use a hard-coded model name, to make it dynamic in the app
# e.g., by adding another args to the function to input model name
result = str(inferrer.infer(document = input_document)[0])
st.write(f"Predicted rating: {result}")
st.write(f"Model used: {model_name}")

# whenever an option is selected in the FE, 
# the var will get assigned the selected value

# st.write(f"Selected trained model: {model_name}")
# select_box = st.selectbox("Select the sub option", 
#              ("option 1",
#               "option 2"))
# st.write(f"Selected option: {select_box}")

# select_box = st.sidebar.selectbox("Select the main option", 
#              ("option A",
#               "option B"))