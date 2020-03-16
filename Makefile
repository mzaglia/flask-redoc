install:
	pip install -U pip
	pip install -e .[tests,docs]

sphinx:
	sphinx-apidoc -o docs/source flask_redoc
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

tests:
	pydocstyle flask_redoc
	isort --check-only --diff --recursive flask_redoc/*.pydocstyle
	check-manifest --ignore ".travis-*" --ignore ".readthedocs.*"
	pytest
