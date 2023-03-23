from flask import Flask, render_template, request, session
from pydantic import BaseModel, validator, ValidationError
from flask import redirect, url_for, flash

app = Flask(__name__)

app.secret_key = 'b\x12\xd2D\xdb\xe9\xd9\x01\xe2,\xfd\xb5\xd6\xa7~\x06\xc7\xe6\xe9\xc1d\xff_\x8e\xa2\x81F\x07\xdc=>\x03\n' 


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

            return redirect(url_for('list_stocks'))
        except ValidationError as e:
            print(e)

    return render_template('add_stock.html')     


@app.route('/stocks/')
def list_stocks():
    return render_template('stocks.html')