#Isael Estrada
#Earth pictures 
import requests
import random
import datetime
import subprocess
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#bootstrap = Bootstrap5(app)


app = Flask(__name__)
bootstrap = Bootstrap5(app)
my_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V'
endpoint = 'https://api.nasa.gov/planetary/earth/imagery'
app.config['SECRET_KEY'] = 'csumb-otter'

#imgs = f"https://api.nasa.gov/planetary/earth/imagery?lon=100.75&lat=1.5&date={earthd}&api_key={my_key}"
#This is where the user input is gonna be stored and added to the url for img
payload = {
    'api_key': my_key
}



earthd="2015-02-01"
earthd2="2015-03-01"
earthd3="2016-02-01"
class EarthForm(FlaskForm):
    earth_date = StringField(
        'Earth Date', 
        validators=[DataRequired()]
    )


def store_date(my_date):
    earthd = my_date



@app.route('/view_playlist')
def vs():
    return render_template('vs.html')