import json
import logging
import math

import requests
import streamlit as st

from streamlit_lottie import st_lottie

@st.cache_resource
def load_assets(url: str) -> dict:
    """Function load asset from a http get request
    Args:
        url (str): URL of the asset to load
    Returns:
        dict: Lottie media json
    """
    # Request the asset from lottie
    asset = requests.get(url)
    # If the request is not successful, return an error
    if asset.status_code != 200:
        logging.error("Failed to load asset")
        return {"Response": "Error"}
    # Otherwise return the json format of the media
    else:
        logging.info("Asset loaded successfully")
        return asset.json()

# Load assets
lottie_flower = load_assets("https://assets10.lottiefiles.com/packages/lf20_vps4jt0g.json")

left, right = st.columns((2, 1))
with left:
    st.title("Iris Classification Web App")

with right:
    # Add a lottie animation
    st_lottie(lottie_flower, key="An animation of a flower")

data = {}

data["Sepal_Length"] = st.number_input(
    "Sepal Length",
    min_value=0.0,
    value=5.1,
    help="The length of the calyx of a flower, enclosing the petals and typically green and leaflike."
)

data["Sepal_Width"] = st.number_input(
    "Sepal Width",
    min_value=0.0,
    value=3.5,
    help="The width of the calyx of a flower, enclosing the petals and typically green and leaflike."
)
data["Petal_Length"] = st.number_input(
    "Petal Length",
    min_value=0.0,
    value=1.4,
    help="The length of the segments of the corolla of a flower, which are modified leaves and are typically coloured."
)
data["Petal_Width"] = st.number_input(
    "Petal_Width",
    min_value=0.0,
    value=0.2,
    help="The width of the segments of the corolla of a flower, which are modified leaves and are typically coloured."
)

if st.button("Classify flower"):
   if not any(math.isnan(v) for v in data.values()):
       data_json = json.dumps(data)

       prediction = requests.post(
           "http://localhost:3000/predict",
           headers={"content-type": "application/json"},
           data = data_json,
       ).text 

       st.write(f"{prediction}")