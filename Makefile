all: test

uninstall:
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

install:
	pip install --upgrade pip twine wheel
	pip install --editable .[dev] --upgrade --use-deprecated=legacy-resolver

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

check-syntax-errors:
	python -m compileall -q .

check-types:
	mypy openfisca_core && mypy openfisca_web_api

check-style: $(filter %.py, $(shell git ls-files))
	@flake8 --select=B,C,E,F,T,W $?

check-style.docs: $(filter openfisca_%.py, $(shell git ls-files))
	@flake8 --select=D,F,R --doctests $?

check-style.tests: $(filter openfisca_%.py, $(shell git ls-files))
	@flake8 --select=A,P --doctests $?

check-style.strict: $(filter %.py, $(shell git ls-files))
	@flake8 \
		--select=A,B,C,D,E,F,P,R,T,W \
		--doctests \
		--max-complexity 5 \
		--max-doc-length 79 \
		--max-line-length 79 \
		$?

format-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	autopep8 `git ls-files | grep "\.py$$"`

test: clean check-syntax-errors check-style check-types
	env PYTEST_ADDOPTS="$$PYTEST_ADDOPTS --cov=openfisca_core" pytest

test.docs: $(filter openfisca_%.py, $(shell git ls-files))
	@${MAKE} clean
	@${MAKE} check-syntax-errors
	@PYTEST_ADDOPTS="$$PYTEST_ADDOPTS --exitfirst" pytest $?
	@${MAKE} check-types
	@${MAKE} check-style.docs
	@${MAKE} check-style.tests

test.strict: $(filter %.py, $(shell git ls-files))
	@${MAKE} clean
	@${MAKE} check-syntax-errors
	@PYTEST_ADDOPTS="$$PYTEST_ADDOPTS --maxfail 5" pytest $?
	@${MAKE} check-types
	@${MAKE} check-style.strict

api:
	openfisca serve --country-package openfisca_country_template --extensions openfisca_extension_template
