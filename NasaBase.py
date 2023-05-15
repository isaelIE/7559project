from flask import Flask,request, render_template
import requests, json
from flask_bootstrap import Bootstrap5
from datetime import timedelta, datetime



app = Flask(__name__)
bootstrap = Bootstrap5(app)


my_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V'






format = '%Y/%m/%d'


#function that takes in date and validates it so that its a valid start date
def validate_date_start(date):
    #does try statement checking for valid date
    try:
        #uses datetime and strptime for validation of date
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        #min date object allowed to start at
        min_date = datetime.strptime("2015-06-13", "%Y-%m-%d")
        return date_obj >= min_date
    except ValueError:
        return False

#validation of date to end at
def validate_date_end(date):

    #validates via using datetime and strptime
    #max date is got by incrementing today() by adding timedelta(1) to get the nextday
    #checks to see if its maxdate or not, if it is then error, otherwise return that value
    try:
        #today = datetime.today().strftime("%Y-%m-%d")
        tommorow = datetime.today() + timedelta(1)
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        max_date = datetime.strptime(tommorow, "%Y-%m-%d")
        return date_obj <= max_date
    except ValueError:
        return False



endpoint = 'https://api.nasa.gov/planetary/apod'

#routes to datepicker nasa_index.html
@app.route('/')
def main():
    return render_template('nasa_index.html')


#routes to nasa_home.html and posts the data that is being passed in
@app.route('/', methods=['POST'])
def my_form_post():

    #takes in form from nasa_index for start date
    variable_start = request.form['date']
    #passes it in to validate_date_start to check if its valid start date
    validate_date_start(variable_start)
    #passes in enddate recieved in form request to validate_date_end to check if its a valid end date
    variable_end = request.form['enddate']
    validate_date_end(variable_end)

    #puts each in datetime format
    datetime_start = datetime.strptime(variable_start, format)
    datetime_end = datetime.strptime(variable_end, format)

    #updates payload with start_date and end_date
    payload = {
    'api_key': my_key,
    'start_date': datetime_start.date(),
    'end_date': datetime_end.date()
    }
    #try statement to try requests to see if works, will work if dates are valid
    try:
        r = requests.get(endpoint, params=payload)
        data = r.json()
        print(data)
    except:
        #try again printed if dates are not valid
        print('please try again')
        #returns data to nasa_home.html to display data
    return render_template('nasa_home.html', data=data)
