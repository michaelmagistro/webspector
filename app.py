from flask import Flask, render_template, request
from datetime import date
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    # Run the webspectre.py scraper using subprocess
    current_date = date.today()
    url = request.form['url']
    subprocess.run(['python', 'webspectre.py', url])
    return render_template('run-scraper.html', current_date=current_date, url=url)

if __name__ == '__main__':
    app.run()