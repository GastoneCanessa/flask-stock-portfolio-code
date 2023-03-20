from flask import Flask, escape, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')   
def about():
    return render_template('about.html', company_name='TestDriven.io') 