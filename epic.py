# Name: Nikhil Kulkarni 
# Class : cst205
from flask import render_template, request
import requests
from datetime import datetime
from math import sqrt

API_KEY = "LajpuMByvnSnptflcjdagHZfhTN6MMDLW7LSEKu0"
BASE_URL = "https://api.nasa.gov/EPIC/api/natural/date/"
# This function makes sure the user enters the correct date.
def validate_date(date):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        min_date = datetime.strptime("2015-06-13", "%Y-%m-%d")
        return date_obj >= min_date
    except ValueError:
        return False
# This function gets the date checks if valid from validate_date function and if valid gets image using GET function.
def get_epic_data(date):
    message = ""
    image_info = None

    if not validate_date(date):
        message = "Please enter a valid date (2015-06-13 or later)."
    else:
        response = requests.get(f"{BASE_URL}{date}?api_key={API_KEY}")
        if response.status_code == 404:
            message = "No image found for the entered date."
        else:
            image_data = response.json()[0]

            image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{date.replace('-', '/')}/png/{image_data['image']}.png"

            sundist = round(sqrt(image_data['sun_j2000_position']['x']**2 + image_data['sun_j2000_position']['y']**2 + image_data['sun_j2000_position']['z']**2) * 0.621371, 2)
            dscovrdist = round(sqrt(image_data['dscovr_j2000_position']['x']**2 + image_data['dscovr_j2000_position']['y']**2 + image_data['dscovr_j2000_position']['z']**2) * 0.621371, 2)
            lunardist = round(sqrt(image_data['lunar_j2000_position']['x']**2 + image_data['lunar_j2000_position']['y']**2 + image_data['lunar_j2000_position']['z']**2) * 0.621371, 2)

            image_info = {
                'url': image_url,
                'date': image_data['date'],
                'caption': image_data['caption'],
                'centroid_coordinates': f"Latitude: {image_data['centroid_coordinates']['lat']}, Longitude: {image_data['centroid_coordinates']['lon']}",
                'sun_distance': f"{sundist} miles",
                'dscovr_distance': f"{dscovrdist} miles",
                'lunar_distance': f"{lunardist} miles"
            }
            return image_info, message
    return None, message
