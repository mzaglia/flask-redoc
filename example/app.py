import os

from flask import Flask
from flask_redoc import Redoc

app = Flask(__name__)

app.config['REDOC'] = {'title':'Petstore'}

redoc = Redoc('petstore.yml', app)

@app.route('/')
def index():
    return "Hello World!"

if __name__ == "__main__":
    app.run()