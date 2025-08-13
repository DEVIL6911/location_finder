# from stsreamlit_folium import folium_static
# import streamlit as st
import folium
import phonenumbers 
from phonenumbers import geocoder
from phonenumbers import carrier
from phonenumbers import timezone
from test import number  # Importing the phone number from test.py
from opencage.geocoder import OpenCageGeocode
Api_key = "YOUR API KEY"    # Replace with your actual OpenCage API key

check_number = phonenumbers.parse(number)  # Replace 'CH' with the appropriate region code if needed
number_location = geocoder.description_for_number(check_number, "en")
print("Location:", number_location)
number_time_zone = timezone.time_zones_for_number(check_number)
number_carrier = carrier.name_for_number(check_number, "en")
service_provider = phonenumbers.parse(number, "RO")
print(carrier.name_for_number(service_provider, "en"))
print("Time Zone:", number_time_zone)
geocoder = OpenCageGeocode(Api_key)
query = str(number_location)
results = geocoder.geocode(query)
if results:     
    lat = results[0]['geometry']['lat']
    lng = results[0]['geometry']['lng']
    print("Latitude:", lat)
    print("Longitude:", lng)   
    map_location = folium.Map(location=[lat, lng], zoom_start=10)
    folium.Marker([lat, lng], popup=number_location).add_to(map_location)  
    map_location.save("location_map.html")  # Save the map to an HTML file
    print("Map has been saved to location_map.html")