from flask import Flask, render_template, request, session
from pydantic import BaseModel, validator, ValidationError
from flask import redirect, url_for, flash
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler

app = Flask(__name__) #we

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


class StockModel(BaseModel):
    """Class for parsing new stock data a form."""
    stock_symbol: str
    number_of_shares: int
    purchase_price: float

    @validator('stock_symbol')
    def stock_symbol_check(cls, value):
        if not value.isalpha() or len(value) > 5:
            raise ValueError('Stock symbol must be 1-5 characters')
        return value.upper()    


@app.route('/')
def index():
    app.logger.info('Calling the index() function.')  # NEW!
    return render_template('index.html')


@app.route('/about')   
def about():
    flash('Thanks for learning about this site!', 'info')
    return render_template('about.html', company_name='TestDriven.io')


@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        # Print the form data to the console
        for key, value in request.form.items():
            print(f'{key}: {value}')

        try:
            stock_data = StockModel(
                stock_symbol=request.form['stock_symbol'],
                number_of_shares=request.form['number_of_shares'],
                purchase_price=request.form['purchase_price']
            )
            print(stock_data)

            # Save the form data to the session object
            session['stock_symbol'] = stock_data.stock_symbol
            session['number_of_shares'] = stock_data.number_of_shares
            session['purchase_price'] = stock_data.purchase_price
            flash(f"Added new stock ({stock_data.stock_symbol})!", 'success')  
            app.logger.info(f"Added new stock ({request.form['stock_symbol']})!") 

            return redirect(url_for('list_stocks'))
        except ValidationError as e:
            print(e)

    return render_template('add_stock.html')     


@app.route('/stocks/')
def list_stocks():
    return render_template('stocks.html')