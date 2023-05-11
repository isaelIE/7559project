from flask import Flask, render_template, request
from marsrover import get_latest_photos, get_rover_info
from epic import get_epic_data
import datetime
import random

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
