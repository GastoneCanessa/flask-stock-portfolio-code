from flask import Flask, render_template, request, session
from pydantic import BaseModel, validator, ValidationError
from flask import redirect, url_for, flash
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__) 

# Configure the Flask application
config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
app.config.from_object(config_type)

app.logger.removeHandler(default_handler)  # serve per non stampare in console i logger

# Logging Configuration
file_handler = RotatingFileHandler('instance/flask-stock-portfolio.log',
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
