import streamlit as st
import datetime
import requests
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut, GeocoderServiceError




'''
# Welcome to TaxiFare
'''


pick_up_address = st.text_input('please enter your pick up location','')


drop_off_address = st.text_input('please enter your drop off location','')


geolocator = Nominatim(user_agent="myApp", timeout=5)

def geocode_address(address):
    if not address or not address.strip():
        return None
    try:
        result = geolocator.geocode(address)
        if result:
            return (result.latitude, result.longitude, result.address)
        return None
    except (GeocoderUnavailable, GeocoderTimedOut, GeocoderServiceError):
        return None


pick_up = geocode_address(pick_up_address)
drop_off = geocode_address(drop_off_address)


# Date and time
ride_datetime = st.datetime_input(
    "Select date and time of the ride",
    value=datetime.datetime.now()
)

# Passenger count
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=8, value=1, step=1)



url = 'https://taxifare.lewagon.ai/predict'

if st.button("Get Fare Prediction"):

    if pick_up is None or drop_off is None:
        st.error("Please enter valid pickup and dropoff addresses.")
    else:
        params = {
            "pickup_datetime": str(ride_datetime),
            "pickup_longitude": pick_up[1],
            "pickup_latitude": pick_up[0],
            "dropoff_longitude": drop_off[1],
            "dropoff_latitude": drop_off[0],
            "passenger_count": passenger_count
        }

        response = requests.get(url, params=params)
        prediction = response.json()
        st.write("Predicted fare:", prediction)
        st.balloons()

map_data = []

if pick_up is not None:
    map_data.append({"latitude": pick_up[0], "longitude": pick_up[1]})

if drop_off is not None:
    map_data.append({"latitude": drop_off[0], "longitude": drop_off[1]})

if map_data:
    df = pd.DataFrame(map_data)
    st.map(df)
