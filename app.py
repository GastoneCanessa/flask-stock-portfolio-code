from flask import Flask, render_template, request, session
from pydantic import BaseModel, validator, ValidationError
from flask import redirect, url_for, flash
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler

app = Flask(__name__) 

app.logger.removeHandler(default_handler)  # serve per non stampare in console i logger

app.secret_key = 'b\x12\xd2D\xdb\xe9\xd9\x01\xe2,\xfd\xb5\xd6\xa7~\x06\xc7\xe6\xe9\xc1d\xff_\x8e\xa2\x81F\x07\xdc=>\x03\n' 

# Logging Configuration
file_handler = RotatingFileHandler('flask-stock-portfolio.log',
                                   maxBytes=16384,
                                   backupCount=20)  # server per creare un altro file di logger quando le dimensioni diventano troppo grandi
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')  
file_handler.setFormatter(file_formatter)  
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

# Log that the Flask application is starting
app.logger.info('Starting the Flask Stock Portfolio App...')


# Import the blueprints
from project.stocks import stocks_blueprint
from project.users import users_blueprint

# Register the blueprints
app.register_blueprint(stocks_blueprint)
app.register_blueprint(users_blueprint, url_prefix='/users')
