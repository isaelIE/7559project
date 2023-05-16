import subprocess
from flask import Flask, render_template, request
from marsrover import get_latest_photos, get_rover_info
from epic import get_epic_data
from Earthy import store_date, EarthForm
import datetime
import random
import sys
import requests
from flask_bootstrap import Bootstrap5
from datetime import timedelta

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = 'csumb-otter'
earthd = "2015-02-01"
earthd2 = "2015-03-01"
earthd3 = "2016-02-01"
my_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V'
format = '%Y-%m-%d'
endpoint = 'https://api.nasa.gov/planetary/apod'

# Your new functions here
def validate_date_start(date):
    try:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        min_date = datetime.datetime.strptime("2015-06-13", "%Y-%m-%d")
        return date_obj >= min_date
    except ValueError:
        return False

def validate_date_end(date):
    try:
        tomorrow = datetime.datetime.today() + timedelta(days=1)
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        max_date = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day)
        return date_obj <= max_date
    except ValueError:
        return False

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/mars_rover', methods=['GET', 'POST'])
def mars_rover():
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

@app.route('/about/<rover_name>', methods=['GET'])
def about(rover_name):
    landing_date, launch_date, status, total_photos = get_rover_info(rover_name)
    return render_template('learnmore.html', rover_name=rover_name, landing_date=landing_date, launch_date=launch_date, status=status, total_photos=total_photos)

@app.route('/nasa_epic', methods=['GET', 'POST'])
def nasa_epic():
    image_info = None
    message = ""

    if request.method == 'POST':
        date = request.form['date']
        image_info, message = get_epic_data(date)

    return render_template('index2.html', message=message, image_info=image_info)


@app.route('/earth_sat', methods=['GET', 'POST'])
def earths():
    date= ""
    form = EarthForm()
    if form.validate_on_submit():
        date=form.earth_date.data
    return render_template('earth.html',form=form, date=date, earthd=earthd, earthd2=earthd2, earthd3=earthd3, my_key=my_key)
    return render_template('earth.html',form=form, earthd=earthd, earthd2=earthd2, earthd3=earthd3, my_key=my_key)

@app.route('/mars_weather')
def mars_weather():
    return render_template('mars.html')

@app.route('/NasaBase', methods=['GET', 'POST'])
def NasaBase():
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if start_date and end_date:
            api_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V' 
            url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}&start_date={start_date}&end_date={end_date}'

            try:
                response = requests.get(url)
                data = response.json()
                return render_template('nasa_home.html', data=data)
            except:
                error_message = 'An error occurred while fetching APOD data.'
                return render_template('nasa_home.html', error=error_message)

    return render_template('nasa_home.html')


if __name__ == '__main__':
    app.run(debug=True)

