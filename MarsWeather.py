import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template
import requests, json
import io
from flask_bootstrap import Bootstrap5
from PIL import Image


#nasa = Client('oGb1FfTXlYV5jwNzjGMKeDJ6s4pvSO54FIqcUw2z')
app = Flask(__name__)
bootstrap = Bootstrap5(app)
url = "https://mars.nasa.gov/rss/api/?feed=weather&category=mars2020&feedtype=json"
data = requests.get(url).json()

print(data['sols'])

figure = plt.figure(figsize=(10,5))




max_temperature =[]
min_temperature =[]

pressure_readings =[]



min_temperature.append(data['sols'][2]['min_temp'])
min_temperature.append(data['sols'][5]['min_temp'])
min_temperature.append(data['sols'][6]['min_temp'])


max_temperature.append(data['sols'][2]['max_temp'])
max_temperature.append(data['sols'][5]['max_temp'])
max_temperature.append(data['sols'][6]['max_temp'])


pressure_readings.append(data['sols'][1]['pressure'])
pressure_readings.append(data['sols'][2]['pressure'])
pressure_readings.append(data['sols'][3]['pressure'])
pressure_readings.append(data['sols'][4]['pressure'])
pressure_readings.append(data['sols'][5]['pressure'])

#print(max_temperature)
#print(min_temperature)

#create a datasheet
data ={"MinTempDay2":min_temperature[0], "MinTempDay5":min_temperature[1],"MinTempDay6":min_temperature[2],"MaxTempDay2":max_temperature[0],"MaxTempDay5":max_temperature[1],"MaxTempDay6":max_temperature[2]}
#data2 ={"PressureReading1":pressure_readings[0], "PressureReading2":pressure_readings[1],"PressureReading3":pressure_readings[2],"PressureReading4":pressure_readings[3], "PressureReading5":pressure_readings[4], "PressureReading6":pressure_readings[5]}
min_temp=list(data.keys())
max_temp=list(data.values())



plt.bar(min_temp, max_temp,color='red',width=0.4)



plt.xlabel("Temperature Readings")
plt.ylabel("Highs and Lows")
plt.title("Mars Weather Temperature Reading")


#pressure_readings = list(data2.keys())
#pressure_readings = list(data2.values())

#plt.xlabel("Pressure Readings")
#plt.ylabel("Pressure throughout days")
#plt.title("Mars Pressure Readings")


#plt.bar(pressure_readings, colo ='blue',width=.4)
#plt.savefig()
fig =plt.gcf()
#plt.savefig('bargraph.png',dpi=300,bbox_inches='tight')
#plt.show()

def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

@app.route('/')
def main():
    img = fig2img(fig)
    return render_template('mars.html', data=img)
