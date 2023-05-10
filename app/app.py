import subprocess
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main_page.html')

@app.route('/app1')
def run_script1():
    subprocess.Popen(['python3.11', 'NasaBase.py'])
    return 'Nasa Base app opened'

# @app.route('/run_script2')
# def run_script2():
#     subprocess.Popen(['python', 'script2.py'])
#     return 'Script 2 executed successfully!'

if __name__ == '__main__':
    app.run(debug=True)