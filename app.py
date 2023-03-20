from flask import Flask, escape

app = Flask(__name__)


@app.route('/hello/<int:message>')
def index(message):
    return f'<h2>The message is: {escape(message)}</h2>'