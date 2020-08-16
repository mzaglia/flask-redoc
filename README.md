# flask-redoc
[![Build Status](https://travis-ci.com/mzaglia/flask-redoc.svg?branch=master)](https://travis-ci.com/mzaglia/flask-redoc)
[![Documentation Status](https://readthedocs.org/projects/flask-redoc/badge/?version=latest)](http://flask-redoc.readthedocs.io/?badge=latest)
[![GitHub license](https://img.shields.io/github/license/mzaglia/flask-redoc)](https://github.com/mzaglia/flask-redoc/blob/master/LICENSE)
[![GitHub tag](https://img.shields.io/github/tag/mzaglia/flask-redoc.svg)](https://github.com/mzaglia/flask-redoc/tags/)
[![PyPI version shields.io](https://img.shields.io/pypi/v/flask-redoc.svg)](https://pypi.python.org/pypi/flask-redoc/)


A Flask extension for displaying OpenAPI/Swagger documentation using Redocs.

# Installation
Under your virtualenv do:

```shell
pip install flask-redoc
```

or (dev version)

```shell
pip install https://github.com/mzaglia/flask-redoc
```

# Getting Started

## Using YAML file
Save your `petstore.yml`
```yaml
openapi: "3.0.0"
info:
  version: 1.0.0
  title: Swagger Petstore
  license:
    name: MIT
servers:
  - url: http://petstore.swagger.io/v1
paths:
  /pets:
    get:
      summary: List all pets
      operationId: listPets
      tags:
        - pets
      parameters:
        - name: limit
          in: query
          description: How many items to return at one time (max 100)
          required: false
          schema:
            type: integer
            format: int32
      responses:
        '200':
          description: A paged array of pets
          headers:
            x-next:
              description: A link to the next page of responses
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Pets"
        default:
          description: unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  schemas:
    Pet:
      type: object
      required:
        - id
        - name
      properties:
        id:
          type: integer
          format: int64
        name:
          type: string
        tag:
          type: string
    Pets:
      type: array
      items:
        $ref: "#/components/schemas/Pet"
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: integer
          format: int32
        message:
          type: string
```

Load in your app:
```python

from flask import Flask
from flask_redoc import Redoc

redoc = Redoc(app,'petstore.yml')

@app.route('/pets', methods=['GET', 'POST'])
def pets():
    ...
```

You can also use docstrings as specification and Marshmallow models for schemas (this will updated any existing specs loaded with YAML files).

```python

app.config['REDOC'] = {'title':'Petstore', 'marshmallow_schemas':[PetSchema]}

class PetSchema(Schema):
    name = fields.Str()

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
```
# Configuration

## Default configuration
```python
 DEFAULT_CONFIG = {
        'endpoint': 'docs',
        'spec_route': '/docs',
        'static_url_path': '/redoc_static',
        'title': 'ReDoc',
        'version': '1.0.0',
        'openapi_version': '3.0.2',
        'info': dict(),
        'marshmallow_schemas': list()
    }
```

## Changing configuration
You can change any default configuration as follows
```python
app.config['REDOC'] = {'spec_route': '/my_docs', 'title': 'My Docs'}
redoc = Redoc(app)
```

# Further reading
For more information about creating your spec using docstring, please visit: https://apispec.readthedocs.io/en/latest/
