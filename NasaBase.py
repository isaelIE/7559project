import sys
import requests, json
from pprint import pprint
from PySide6.QtWidgets import (QApplication, QLabel, QWidget, QPushButton, QLabel, QVBoxLayout, QDateEdit)
from PySide6.QtCore import Slot, QDate, Qt   
from PySide6.QtGui import QPixmap
from qt_material import apply_stylesheet


my_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V'
endpoint = 'https://api.nasa.gov/planetary/apod'

payload = {
    'api_key': my_key,
    'start_date': '2023-03-09',
    'end_date': '2023-03-11'
}

# try:
#     r = requests.get(endpoint, params=payload)
#     if r.ok:
#         data = r.json()
#         pprint(data)
# except Exception as e:
#     print(e)
#     print('please try again')           


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()
        self.my_lbl = QLabel('<h1>Search NASA Astronomy Photo of the Day</h1>')
        self.pixmap = QPixmap()
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat('yyyy-MM-dd')
        self.date_edit.setCalendarPopup(True)
        self.my_btn = QPushButton("Search")
        self.my_btn.clicked.connect(self.on_click)
        vbox.addWidget(self.my_lbl)
        vbox.addWidget(self.date_edit)
        vbox.addWidget(self.my_btn)
        self.setLayout(vbox)
        self.resize(800, 600)

    @Slot()
    def on_click(self):

        value = self.date_edit.date()
        print(str(value))
   
        payload = {
            'api_key': my_key,
            'start_date': f'{value.year()}-{value.month()}-{value.day()}',
            'end_date': f'{value.year()}-{value.month()}-{value.day()}'
        }

        try:
            r = requests.get(endpoint, params=payload)
            if r.ok:
                data = r.json()
                pprint(data)
                url = data[0]['url']
                print(url)
                if url[-4:] == '.jpg' or url[4:] == '.png':
                    self.img_from_url(url)
                else:
                    print("not a jpg or png")
                    self.img_from_url(data[1]['url'])
        except Exception as e:
            print(e)
            self.my_lbl.setText('<h1>Please try again</h1>')
  

    def img_from_url(self, url):
        try:
            img = requests.get(url)
            if img.ok:
                print("img ok")
                self.pixmap.loadFromData(img.content)
                print(self.pixmap)
                self.pixmap = self.pixmap.scaled(800, 600, Qt.KeepAspectRatio)
                self.my_lbl.setPixmap(self.pixmap)
        except Exception as e:
            print(e)
            self.my_lbl.setText('<h1>Please try this again</h1>')
 

app = QApplication([])
apply_stylesheet(app, theme='dark_teal.xml')

my_win = MyWindow()
my_win.show()
sys.exit(app.exec())

