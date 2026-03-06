import streamlit as st
import datetime
import requests
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np

'''
# Welcome to TaxiFare
'''

st.title("please enter the parameters of your ride :) ")

pick_up_address = st.text_input('please enter your pick up location', '412 Macon Street,Brooklyn,NY,11233')
st.write('your current location is', pick_up_address)


drop_off_address = st.text_input('please enter your drop off location', '1123 East Tremont Avenue,Bronx,NY,10460')
st.write('you want to go to', drop_off_address)

pick_up_address= '412 Macon Street,Brooklyn,NY,11233'
drop_off_address='1123 East Tremont Avenue,Bronx,NY,10460'

geolocator = Nominatim(user_agent="myApp")
df = pd.DataFrame({'Location':
             [pick_up_address, drop_off_address]})

df[['latitude', 'longitude']] =  df['Location'].apply(
    geolocator.geocode).apply(lambda x: pd.Series(
        [x.latitude, x.longitude], index=['location_lat', 'location_long']))

def get_map_data():

    return df[['latitude', 'longitude']]

df = get_map_data()
st.map(df)



# Date and time
ride_datetime = st.datetime_input(
    "Select date and time of the ride",
    value=datetime.datetime.now()
)

# Passenger count
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=8, value=1, step=1)

st.write("Ride details:", {
    "datetime": ride_datetime,
    "pickup_longitude": df['longitude'][0],
    "pickup_latitude": df['latitude'][0],
    "dropoff_longitude": df['longitude'][1],
    "dropoff_latitude": df['latitude'][1],
    "passenger_count": passenger_count
})
'''
## Please press the below button to get the predicted price of your ride
'''''


url = 'https://taxifare.lewagon.ai/predict'

if st.button("Get Fare Prediction"):
    params = {
        "pickup_datetime": str(ride_datetime),
        "pickup_longitude": df['longitude'][0],
        "pickup_latitude": df['latitude'][0],
        "dropoff_longitude": df['longitude'][1],
        "dropoff_latitude": df['latitude'][1],
        "passenger_count": passenger_count
    }
    response = requests.get(url, params=params)
    prediction = response.json()
    st.write("Predicted fare:", prediction)
