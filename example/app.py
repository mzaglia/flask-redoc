import os

from flask import Flask
from flask_redoc import Redoc
from marshmallow import Schema, fields

class PetSchema(Schema):
    name = fields.Str()

app = Flask(__name__)

app.config['REDOC'] = {'title':'Petstore', 'marshmallow_schemas':[PetSchema]}

redoc = Redoc(app,'petstore.yml')


@app.route('/')
def index():
    return "Hello World!"


@app.route('/random')
def random():
    """A cute furry animal endpoint.
    ---
    get:
      description: Get a random pet
      responses:
        200:
          description: Return a pet
          content:
            application/json:
              schema: PetSchema
    """
    return PetSchema().dump(dict(name="Bird"))


if __name__ == "__main__":
    app.run()
