import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template
import requests, json
import io
from flask_bootstrap import Bootstrap5
from PIL import Image



app = Flask(__name__)
bootstrap = Bootstrap5(app)
#url used for mars weather api
url = "https://mars.nasa.gov/rss/api/?feed=weather&category=mars2020&feedtype=json"
#data requested via url request and translated via json
data = requests.get(url).json()

#print(data['sols'])

#figure plot made  and figuresize established
figure = plt.figure(figsize=(10,5))



#max, min , and pressure_readings for the data sets via lists  
max_temperature =[]
min_temperature =[]
pressure_readings =[]


#grabs min temp data and adds to list
min_temperature.append(data['sols'][2]['min_temp'])
min_temperature.append(data['sols'][5]['min_temp'])
min_temperature.append(data['sols'][6]['min_temp'])

#grabs max temp data adds to list
max_temperature.append(data['sols'][2]['max_temp'])
max_temperature.append(data['sols'][5]['max_temp'])
max_temperature.append(data['sols'][6]['max_temp'])

#grabs pressure reading adds to list
pressure_readings.append(data['sols'][1]['pressure'])
pressure_readings.append(data['sols'][2]['pressure'])
pressure_readings.append(data['sols'][3]['pressure'])
pressure_readings.append(data['sols'][4]['pressure'])
pressure_readings.append(data['sols'][5]['pressure'])


#create a datasheet for 2 graphs
data ={"MinTempDay2":min_temperature[0], "MinTempDay5":min_temperature[1],"MinTempDay6":min_temperature[2],"MaxTempDay2":max_temperature[0],"MaxTempDay5":max_temperature[1],"MaxTempDay6":max_temperature[2]}
data2 ={"PressureReading1":pressure_readings[0], "PressureReading2":pressure_readings[1],"PressureReading3":pressure_readings[2],"PressureReading4":pressure_readings[3], "PressureReading5":pressure_readings[4]}
#gets data keys and, values for min_temp and max_temp
min_temp=list(data.keys())
max_temp=list(data.values())

#r1 = np.arange(5)
#plt.subplot(1, 2, 2)
#plt.bar(r1,min_temp, max_temp,color='red')
#plt.xlabel("Temperature Readings")
#plt.ylabel("Highs and Lows")
#plt.title("Mars Weather Temperature Reading")
#plt.show()

#gets the pressure readings keys and values
pressure_readings = list(data2.keys())
pressure_readings = list(data2.values())
#plots x,y and title labels
plt.xlabel("Pressure Readings")
plt.ylabel("Pressure throughout days")
plt.title("Mars Pressure Readings")
days =[1,2,3,4,5]
#plt.subplot(1,2,1)
#plots bar graph
plt.bar( days, pressure_readings, color ='blue',width=.4)

fig =plt.gcf()
#plt.savefig('bargraph.png',dpi=300,bbox_inches='tight')
#plt.show()

#converts figure bar graph to image
def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img
#passes in image data to render_template displayed in mars.html
@app.route('/')
def main():
    img = fig2img(fig)
    return render_template('mars.html', data=img)
