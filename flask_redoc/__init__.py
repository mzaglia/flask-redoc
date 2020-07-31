"""flask_redoc Module."""
import copy
import json
import os

import yaml
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Blueprint, render_template
from jsonmerge import merge

from .version import __version__


class Redoc(object):
    """Redoc Object."""

    DEFAULT_CONFIG = {
        'endpoint': 'docs',
        'spec_route': '/docs',
        'static_url_path': '/redoc_static',
        'title': 'ReDoc',
        'version': '1.0.0',
        'openapi_version': '3.0.2',
        'use_cdn': True,
        'info':dict(),
        'plugins': [FlaskPlugin()],
        'marshmallow_schemas': list()
    }

    def __init__(self, app=None, spec_file=None, config=None):
        """Init the Redoc object.

        :param spec_file: spec file path
        :param app: Flask app
        :param config: dictionary with Redoc configuration
        """
        self.app = app
        self.spec_file = spec_file
        self.config = config or self.DEFAULT_CONFIG.copy()
        self.spec = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the Redoc.

        :param app: Flask app
        """
        self.app = app

        self.config.update(self.app.config.get('REDOC', {}))

        if len(self.config['marshmallow_schemas']) > 0:
            self.config['plugins'].append(MarshmallowPlugin())

        if self.spec_file is not None:
            self.spec_file = self.load_spec_file(self.spec_file)
            self.config['title'] = self.spec_file['info']['title']
            self.config['version'] = self.spec_file['info']['version']
            self.config['openapi_version'] = self.spec_file['openapi']
            self.config['info'] = self.spec_file['info']

        self.spec = APISpec(title=self.config['title'],
                            version=self.config['version'],
                            openapi_version=self.config['openapi_version'],
                            info=self.config['info'],
                            plugins=self.config['plugins'])

        self.app.before_first_request(self.docstrings_to_openapi)


        bp = Blueprint(self.config.get('endpoint', 'redoc'),
                       __name__,
                       url_prefix=self.config.get('url_prefix', None),
                       template_folder=self.config.get(
                           'template_folder', 'templates'),
                       static_folder=self.config.get(
                           'static_folder', 'static'),
                       static_url_path=self.config.get('static_url_path'))

        bp.add_url_rule(self.config.get('spec_route'),
                        'docs', view_func=self.docs_view)
        bp.add_url_rule(self.config.get('spec_route')+'/json',
                        'docs_json', view_func=self.docs_json)

        self.app.register_blueprint(bp)

    def docs_view(self):
        """Render the docs.html template."""
        return render_template('docs.html',
                               spec_file=self.spec_file,
                               endpoint=self.config.get('endpoint', 'redoc'),
                               title=self.config.get('title', 'ReDoc'),
                               use_cdn=self.config.get('use_cdn', True))
    def docs_json(self):
        return self.spec_file

    def load_spec_file(self, filename):
        """Load the spec file.

        :param filename: spec filename

        :return: spec as dict
        """
        if not filename.startswith('/'):
            filename = os.path.join(
                self.app.root_path,
                filename
            )
        with open(filename) as file:
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                retval = yaml.safe_load(file)
            else:
                retval = json.load(file)
        return retval

    def docstrings_to_openapi(self):
        """Transform Flask docstring documentation to openapi spec.
        """

        for schema in self.config['marshmallow_schemas']:
            self.spec.components.schema(schema.__name__, schema=schema)

        for view_name, view_func in self.app.view_functions.items():
            if view_func.__doc__ is not None:
                self.spec.path(view=view_func)


        self.spec_file = strip_empties_from_dict(merge(self.spec_file, self.spec.to_dict()))


def strip_empties_from_list(data):
    """Strip empty list
    """
    new_data = []
    for v in data:
        if isinstance(v, dict):
            v = strip_empties_from_dict(v)
        elif isinstance(v, list):
            v = strip_empties_from_list(v)
        if v not in (None, str(), list(), dict(),):
            new_data.append(v)
    return new_data


def strip_empties_from_dict(data):
    """Strip empty dict
    """
    new_data = {}
    for k, v in data.items():
        if isinstance(v, dict):
            v = strip_empties_from_dict(v)
        elif isinstance(v, list):
            v = strip_empties_from_list(v)
        if v not in (None, str(), list(), dict(),):
            new_data[k] = v
    return new_data
