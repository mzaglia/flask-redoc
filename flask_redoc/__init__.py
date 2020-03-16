"""flask_redoc Module."""
import json
import os

import yaml
from flask import Blueprint, render_template

from .version import __version__


class Redoc(object):
    """Redoc Object."""

    DEFAULT_CONFIG = {
        'endpoint': 'docs',
        'spec_route': '/docs',
        'static_url_path': '/redoc_static',
        'title': 'ReDoc',
        'use_cdn': True
    }

    def __init__(self, spec_file, app=None, config=None):
        """Init the Redoc object.

        :param spec_file: spec file path
        :param app: Flask app
        :param config: dictionary with Redoc configuration
        """
        self.app = app
        self.spec_file = spec_file
        self.config = config or self.DEFAULT_CONFIG.copy()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the Redoc.

        :param app: Flask app
        """
        self.app = app

        self.config.update(self.app.config.get('REDOC', {}))

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

        self.app.register_blueprint(bp)

    def docs_view(self):
        """Render the docs.html template."""
        return render_template('docs.html',
                               spec_file=self.load_spec_file(self.spec_file),
                               endpoint=self.config.get('endpoint', 'redoc'),
                               title=self.config.get('title', 'ReDoc'),
                               use_cdn=self.config.get('use_cdn', True))

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
