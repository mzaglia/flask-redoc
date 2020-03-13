import pytest
from flask import Flask
from flask_redoc import Redoc

class TestFlaskRedoc:

    def test_redoc_yml(self):
        app = Flask(__name__)
        client = app.test_client()
        Redoc('petstore.yml', app)
        resp = client.get('/docs')
        assert resp.status_code == 200

    def test_redoc_json(self):
        app = Flask(__name__)
        client = app.test_client()
        Redoc('petstore.json', app)
        resp = client.get('/docs')
        assert resp.status_code == 200