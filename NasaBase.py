from flask import Flask, render_template
import requests, json
from flask_bootstrap import Bootstrap5
from datetime import date
import datetime

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# better to replace this with your own key from https://api.nasa.gov/
my_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V'

val = input("Enter the starting date value you want to see Nasa's picture of the day: ") 

val_two = input("Enter the end date value you want to see Nasa's picture of the day: ") 


format = '%Y/%m/%d'

datetime_start = datetime.datetime.strptime(val, format)
datetime_end = datetime.datetime.strptime(val_two, format)

payload = {
  'api_key': my_key,
  'start_date': datetime_start.date(),
  'end_date': datetime_end.date()
}

endpoint = 'https://api.nasa.gov/planetary/apod'

@app.route('/')
def main():
    try:
        r = requests.get(endpoint, params=payload)
        data = r.json()
        print(data)
    except:
        print('please try again')
    return render_template('nasa_home.html', data=data)
