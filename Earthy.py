#Isael Estrada
#Earth pictures 
import requests
import random
import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5

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


#@app.route('/', methods=('GET', 'POST'))
#def earth():
#    form = EarthForm()
#    store_date(form.earth_date.data)
#    if form.validate_on_submit():
#        store_date(form.earth_date.data)
#        return redirect('/view_playlist')
#    return render_template('earth.html', form=form, earthd=earthd, earthd2=earthd2, earthd3=earthd3, my_key=my_key)

@app.route('/', methods=('GET', 'POST'))
def earths():
    date= ""
    form = EarthForm()
    if form.validate_on_submit():
        date=form.earth_date.data
        return render_template('earth.html',form=form, date=date, earthd=earthd, earthd2=earthd2, earthd3=earthd3, my_key=my_key)
    return render_template('earth.html',form=form, earthd=earthd, earthd2=earthd2, earthd3=earthd3, my_key=my_key)

@app.route('/view_playlist')
def vs():
    return render_template('vs.html')