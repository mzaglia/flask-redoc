import os

from setuptools import setup, find_packages

readme = open('README.md').read()

docs_require = [
    'Sphinx>=2.2',
]

tests_require = [
    'coverage>=4.5',
    'coveralls>=1.8',
    'pytest>=5.2',
    'pytest-cov>=2.8',
    'pytest-pep8>=1.0',
    'pydocstyle>=4.0',
    'isort>4.3',
    'check-manifest>=0.40',
]

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
}

extras_require['all'] = [req for exts, reqs in extras_require.items()
                         for req in reqs]

setup_requires = [
    'pytest-runner>=5.2',
]

with open(os.path.join('flask_redoc', 'version.py'), 'rt') as fp:
    g = {}
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='flask_redoc',
    version=version,
    url='https://github.com/mzaglia/flask-redoc',
    license='MIT',
    author='Matheus C. Zaglia',
    author_email='mzaglia@gmail.com',
    description=__doc__,
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=list(filter(lambda pkg: 'tests' not in pkg, find_packages())),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    extras_require=extras_require,
    setup_requires=setup_requires,
    tests_require=tests_require,
    install_requires=['Flask>=1.1.1',
                      'PyYAML>=5.3',
                      'apispec>=3.3.1',
                      'apispec-webframeworks>=0.5.2',
                      'jsonmerge>=1.7.0',
                      'marshmallow>=3.6.1'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
