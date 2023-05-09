import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template
import requests, json
from flask_bootstrap import Bootstrap5

#nasa = Client('oGb1FfTXlYV5jwNzjGMKeDJ6s4pvSO54FIqcUw2z')
app = Flask(__name__)
bootstrap = Bootstrap5(app)
url = "https://mars.nasa.gov/rss/api/?feed=weather&category=mars2020&feedtype=json"
data = requests.get(url).json()

print(data['sols'])

figure = plt.figure(figsize=(10,5))




max_temperature =[]
min_temperature =[]


min_temperature.append(data['sols'][2]['min_temp'])
min_temperature.append(data['sols'][5]['min_temp'])
min_temperature.append(data['sols'][6]['min_temp'])


max_temperature.append(data['sols'][2]['max_temp'])
max_temperature.append(data['sols'][5]['max_temp'])
max_temperature.append(data['sols'][6]['max_temp'])

#print(max_temperature)
#print(min_temperature)

#create a datasheet
data ={"MinTempDay2":min_temperature[0], "MinTempDay5":min_temperature[1],"MinTempDay6":min_temperature[2],"MaxTempDay2":max_temperature[0],"MaxTempDay5":max_temperature[1],"MaxTempDay6":max_temperature[2]}

min_temp=list(data.keys())
max_temp=list(data.values())


plt.bar(min_temp, max_temp,color='red',width=0.4)


plt.xlabel("Temperature Readings")
plt.ylabel("Highs and Lows")
plt.title("Mars Weather Temperature Reading")

plt.savefig('bargraph.png',dpi=300,bbox_inches='tight')
plt.show()

#@app.route('/')
#def main():

 #   return render_template('mars.html', data=)
