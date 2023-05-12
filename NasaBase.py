from flask import Flask,request, render_template
import requests, json
from flask_bootstrap import Bootstrap5
from datetime import datetime



app = Flask(__name__)
bootstrap = Bootstrap5(app)

# better to replace this with your own key from https://api.nasa.gov/
my_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V'






format = '%Y/%m/%d'



def validate_date_start(date):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        min_date = datetime.strptime("2015-06-13", "%Y-%m-%d")
        return date_obj >= min_date
    except ValueError:
        return False

def validate_date_end(date):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        max_date = datetime.strptime(date.today(), "%Y-%m-%d")
        return date_obj <= max_date
    except ValueError:
        return False



endpoint = 'https://api.nasa.gov/planetary/apod'

@app.route('/')
def main():
    return render_template('nasa_index.html')


@app.route('/', methods=['POST'])
def my_form_post():

    variable_start = request.form['date']
    validate_date_start(variable_start)
    variable_end = request.form['enddate']

    datetime_start = datetime.strptime(variable_start, format)
    datetime_end = datetime.strptime(variable_end, format)
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

