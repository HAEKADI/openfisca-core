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
	@flake8 \
		--select=B,C,E,F,T,W, \
		${args} \
		$?

check-style.docs:
	@${MAKE} \
		check-style \
		args="--doctests"

check-style.strict:
	@${MAKE} \
		check-style \
		args=" \
			--max-complexity 5 \
			--max-doc-length 79 \
			--max-line-length 79 \
			"

format-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	autopep8 `git ls-files | grep "\.py$$"`

test: clean check-syntax-errors check-style check-types
	env PYTEST_ADDOPTS="$$PYTEST_ADDOPTS --cov=openfisca_core" pytest

api:
	openfisca serve --country-package openfisca_country_template --extensions openfisca_extension_template
