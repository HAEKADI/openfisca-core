OK := "\033[0;32m OK! \033[0m"
PASS := "\033[0;33m PASS \033[0m"
COUNTRY_TEMPLATE := openfisca_country_template
EXTENSION_TEMPLATE := openfisca_extension_template
PYTHON_PACKAGES_PATH := $(shell python -c "import sysconfig; print(sysconfig.get_paths()[\"purelib\"])")
COUNTRY_TEMPLATE_TESTS := ${PYTHON_PACKAGES_PATH}/${COUNTRY_TEMPLATE}/tests
EXTENSION_TEMPLATE_TESTS := ${PYTHON_PACKAGES_PATH}/${EXTENSION_TEMPLATE}/tests

all: test

## List all the available tasks.
help:
	@## See https://gist.github.com/klmr/575726c7e05d8780505a.
	@sed -ne "/^## /{h;s/.*//;:d" -e "H;n;s/^## //;td" -e "s/:.*//;G;s/\\n## /---/;s/\\n/ /g;p;}" ${MAKEFILE_LIST} | awk -F --- -v n=$$(tput cols) -v i=19 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"%s%*s%s ",a,-i,$$1,z;m=split($$2,w," ");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;printf"\n%*s ",-i," ";}printf"%s ",w[j];}printf"\n";}'

uninstall:
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

install:
	pip install --upgrade pip twine wheel
	pip install --editable .[dev] --upgrade --use-deprecated=legacy-resolver

## Delete builds and compiled python files.
clean:: ;

clean:: $(shell find . -name "*.pyc")
	@printf "Deleting compiled files..."
	@[ ! -z "$?" ] \
		&& { rm -f $? && echo ${OK} ; } \
		|| echo ${PASS}

clean:: $(shell ls -d * | grep "build\|dist")
	@printf "Deleting builds..."
	@[ ! -z "$?" ] \
		&& { rm -rf $? && echo ${OK} ; } \
		|| echo ${PASS}

## Compile python files to check for syntax errors.
check-syntax-errors:
	@printf "Compiling python files..."
	@python -m compileall -q .
	@echo ${OK}

## Run linters to check for syntax and style errors.
check-style: $(shell git ls-files | grep "\.py$$")
	@## Do not analyse .gitignored files.
	@## `make` needs `$$` to output `$`.
	@## See http://stackoverflow.com/questions/2382764.
	@printf "Running linters..."
	@flake8 $? &> /tmp/result; echo $$? > /tmp/status;
	@[ $$(</tmp/status) -eq 0 ] \
		&& echo ${OK} \
		|| { echo "\n$$(cat /tmp/result)" && exit $$(</tmp/status) ; }

## Run static type checkers for type errors.
check-types: $(shell ls -d * | grep "openfisca_")
	@printf "Running static type checkers..."
	@mypy $? &> /tmp/result; echo $$? > /tmp/status;
	@[ $$(</tmp/status) -eq 0 ] \
		&& echo ${OK} \
		|| { echo "\n$$(cat /tmp/result)" && exit $$(</tmp/status) ; }

## Run code formatters to correct style errors.
format-style: $(shell git ls-files | grep "\.py$$")
	@## Do not analyse .gitignored files.
	@## `make` needs `$$` to output `$`.
	@## See http://stackoverflow.com/questions/2382764.
	@printf "Running code formatters..."
	@autopep8 $?
	@echo ${OK}

## Run openfisca-core & country/extension template tests.
test: clean check-syntax-errors check-style check-types
	@##	Usage:
	@##
	@##		make test [pytest_args="--ARG"] [openfisca_args="--ARG"]
	@##
	@##	Examples:
	@##
	@##		make test pytest_args="--exitfirst"
	@##		make test openfisca_args="--performance"
	@##		make test pytest_args="--exitfirst" openfisca_args="--performance"
	PYTEST_ADDOPTS="$$PYTEST_ADDOPTS ${pytest_args}" pytest
	PYTEST_ADDOPTS="$$PYTEST_ADDOPTS ${pytest_args}" openfisca test ${COUNTRY_TEMPLATE_TESTS} --country-package ${COUNTRY_TEMPLATE} ${openfisca_args}
	PYTEST_ADDOPTS="$$PYTEST_ADDOPTS ${pytest_args}" openfisca test ${EXTENSION_TEMPLATE_TESTS} --country-package ${COUNTRY_TEMPLATE} --extensions ${EXTENSION_TEMPLATE} ${openfisca_args}

serve:
	openfisca serve -c ${COUNTRY_TEMPLATE} -e ${EXTENSION_TEMPLATE} ${optional_arguments}
