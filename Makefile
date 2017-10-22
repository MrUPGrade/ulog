SHELL::=/bin/bash
RM=rm -Rfv
PYTHON=python
PYTEST=pytest
PIP::=pip

clean-pyc:
	find . -name '*.pyc' -exec rm -fv {} +
	find . -name '*.pyo' -exec rm -fv {} +

clean-test:
	$(RM) .cache
	$(RM) .coverage

clean: clean-pyc clean-test
	$(RM) *.log
	$(RM) *.egg-info
	$(RM) graph_output
	$(RM) artifacts
	$(RM) build/
	$(RM) dist/

pip-install:
	$(PIP) install --upgrade -e .[dev,test]

test: clean-test clean-pyc
	$(PYTEST)

test-cov: clean-test clean-pyc
	$(PYTEST) --cov

build-pkg:
	$(PYTHON) setup.py bdist_wheel --universal

pypi-upload:
	$(PYTHON) setup.py bdist_wheel --universal upload