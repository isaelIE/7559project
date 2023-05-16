# Name: Nikhil Kulkarni 
# Class : cst205
import requests
import random
import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

API_KEY = 'LajpuMByvnSnptflcjdagHZfhTN6MMDLW7LSEKu0'
# This function below gets info about the rover using the GET function.
def get_rover_info(rover_name):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()['rover']
    landing_date = data['landing_date']
    status = data['status']
    launch_date = data['launch_date']
    total_photos = data['total_photos']
    return landing_date, launch_date, status, total_photos
# This function retrives photos from the rover.
def get_latest_photos(rover_name):
    if rover_name == "perseverance":
        sol = random.randint(0, 448)
    else:
        sol = random.randint(1, 3000)
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?sol={sol}&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    latest_photos = {}
    for photo in data['photos']:
        camera_name = photo['camera']['name']
        if camera_name not in latest_photos:
            latest_photos[camera_name] = photo
    return latest_photos
# routes to home page using get/post method.
@app.route('/', methods=['GET', 'POST'])
def nasarover():
    photos = []
    rover_name = ''
    if request.method == 'POST':
        rover_name = request.form['rover']
        latest_photos = get_latest_photos(rover_name)
        while len(photos) < 7 and len(latest_photos) > 0:
            photo = random.choice(list(latest_photos.values()))
            earth_time = datetime.datetime.strptime(photo['earth_date'], "%Y-%m-%d")
            photo['earth_time'] = earth_time.strftime("%m/%d/%Y")
            photos.append(photo)
            del latest_photos[photo['camera']['name']]
        return render_template('roverphotos.html', photos=photos, rover_name=rover_name)
    return render_template('roverphotos.html', photos=photos)
# This routes to an about page where you can see detailed info about the rover.
@app.route('/about/<rover_name>', methods=['GET'])
def about(rover_name):
    landing_date, launch_date, status, total_photos = get_rover_info(rover_name)
    return render_template('learnmore.html', rover_name=rover_name, landing_date=landing_date, launch_date=launch_date, status=status, total_photos=total_photos)

