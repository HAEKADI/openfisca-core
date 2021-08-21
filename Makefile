COUNTRY_TEMPLATE := openfisca_country_template
EXTENSION_TEMPLATE := openfisca_extension_template
PYTHON_PACKAGES_PATH := $(shell python -c "import sysconfig; print(sysconfig.get_paths()[\"purelib\"])")
COUNTRY_TEMPLATE_TESTS := ${PYTHON_PACKAGES_PATH}/${COUNTRY_TEMPLATE}/tests
EXTENSION_TEMPLATE_TESTS := ${PYTHON_PACKAGES_PATH}/${EXTENSION_TEMPLATE}/tests

all: test

uninstall:
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

install:
	pip install --upgrade pip twine wheel
	pip install --editable .[dev] --upgrade --use-deprecated=legacy-resolver

clean:
	rm -rf build dist
	find . -name "*.pyc" -exec rm \{\} \;

check-syntax-errors:
	python -m compileall -q .

check-types:
	mypy openfisca_core && mypy openfisca_web_api

check-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	flake8 `git ls-files | grep "\.py$$"`

format-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	autopep8 `git ls-files | grep "\.py$$"`

test: clean check-syntax-errors check-style check-types
	PYTEST_ADDOPTS="$$PYTEST_ADDOPTS ${pytest_args}" pytest
	PYTEST_ADDOPTS="$$PYTEST_ADDOPTS ${pytest_args}" openfisca test ${COUNTRY_TEMPLATE_TESTS} --country-package ${COUNTRY_TEMPLATE} ${openfisca_args}
	PYTEST_ADDOPTS="$$PYTEST_ADDOPTS ${pytest_args}" openfisca test ${EXTENSION_TEMPLATE_TESTS} --country-package ${COUNTRY_TEMPLATE} --extensions ${EXTENSION_TEMPLATE} ${openfisca_args}

serve:
	openfisca serve -c ${COUNTRY_TEMPLATE} -e ${EXTENSION_TEMPLATE} ${optional_arguments}
