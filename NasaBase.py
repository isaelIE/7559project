from flask import Flask,request, render_template
import requests, json
from flask_bootstrap import Bootstrap5
from datetime import timedelta, datetime



app = Flask(__name__)
bootstrap = Bootstrap5(app)


my_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V'

endpoint = 'https://api.nasa.gov/planetary/apod'

#routes to datepicker nasa_index.html
@app.route('/')
def main():
    return render_template('nasa_index.html')


#routes to nasa_home.html and posts the data that is being passed in
@app.route('/NasaBase', methods=['GET','POST'])
def NasaBase():
    #checks for a post
    if request.method == 'POST':
        #gets the start and end date from the form
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        #checks for start and end date
        if start_date and end_date:
            #api key being used and url thats being used for the requests
            api_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V'
            url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}&start_date={start_date}&end_date={end_date}'
            #try statement to see if the data is valid from the response
            try:
                response = requests.get(url)
                data = response.json()
                return render_template('nasa_home.html', data=data)
            except:
                #if not valid error will occur and the error message will be displayed on webpage
                error_message = 'An error occurred while fetching APOD data.'
                return render_template('nasa_home.html', error=error_message)

    return render_template('nasa_home.html')
