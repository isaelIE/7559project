from flask import Flask,request, render_template
import requests, json
from flask_bootstrap import Bootstrap5
from datetime import date
import datetime


app = Flask(__name__)
bootstrap = Bootstrap5(app)

# better to replace this with your own key from https://api.nasa.gov/
my_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V'






format = '%Y/%m/%d'




endpoint = 'https://api.nasa.gov/planetary/apod'

@app.route('/')
def main():
    return render_template('nasa_index.html')


@app.route('/', methods=['POST'])
def my_form_post():

    variable = request.form['date']
    datetime_start = datetime.datetime.strptime(variable, format)
    datetime_end = datetime.datetime.strptime(variable, format)
    payload = {
    'api_key': my_key,
    'start_date': datetime_start.date(),
    'end_date': datetime_end.date()
    }
    try:
        r = requests.get(endpoint, params=payload)
        data = r.json()
        print(data)
    except:
        print('please try again')
    return render_template('nasa_home.html', data=data)

