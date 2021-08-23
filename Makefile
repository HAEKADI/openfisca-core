OK := "$$(tput setaf 2) [✓] $$(tput sgr0)"
KO := "$$(tput setaf 1) [!] $$(tput sgr0)"
PASS := "$$(tput setaf 3) [~] $$(tput sgr0)"
WORKING := "$$(tput setaf 5)[⚙]$$(tput sgr0)"
OPTIONS := "$$(tput setaf 6)[ℹ]$$(tput sgr0)"
WARNINGS = "$$(tput setaf 3)[ℹ]$1$$(tput sgr0)"
COUNTRY_TEMPLATE := openfisca_country_template
EXTENSION_TEMPLATE := openfisca_extension_template
PYTHON_PACKAGES_PATH := $$(python -c "import sysconfig; print(sysconfig.get_paths()[\"purelib\"])")
COUNTRY_TEMPLATE_TESTS := ${PYTHON_PACKAGES_PATH}/${COUNTRY_TEMPLATE}/tests
EXTENSION_TEMPLATE_TESTS := ${PYTHON_PACKAGES_PATH}/${EXTENSION_TEMPLATE}/tests

all: test

## List all the available tasks.
help:
	@## See https://gist.github.com/klmr/575726c7e05d8780505a.
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}'

## Uninstall project dependencies.
uninstall:
	@echo "${WORKING} Uninstalling dependencies..."
	@pip freeze | grep -v "^-e" | xargs pip uninstall -y

## Install project dependencies.
install:
	@echo "${WORKING} Installing dependencies..."
	@pip install --upgrade pip twine wheel
	@pip install --editable .[dev] --upgrade --use-deprecated=legacy-resolver

## Delete builds and compiled python files.
clean:: ;

clean:: $(shell find . -name "*.pyc")
	@printf "${WORKING} Deleting compiled files..."
	@[ ! -z "$?" ] \
		&& rm -f $? \
		&& echo ${OK} \
		|| echo ${PASS}

clean:: $(shell ls -d * | grep "build\|dist")
	@printf "${WORKING} Deleting builds..."
	@[ ! -z "$?" ] \
		&& rm -rf $? \
		&& echo ${OK} \
		|| echo ${PASS}

## Compile python files to check for syntax errors.
check-syntax-errors:
	@printf "${WORKING} Compiling python files..."
	@python -m compileall -q .
	@echo ${OK}

## Run linters to check for syntax and style errors.
check-style: $(shell git ls-files | grep "\.py$$")
	@## Do not analyse .gitignored files.
	@## `make` needs `$$` to output `$`.
	@## See http://stackoverflow.com/questions/2382764.
	@printf "${WORKING} Running linters..."
	@flake8 $? &> /tmp/result; echo $$? > /tmp/status;
	@[ $$(</tmp/status) -eq 0 ] \
		&& echo ${OK} \
		|| echo "${KO}\n$$(</tmp/result)" \
		&& exit $$(</tmp/status)

## Run static type checkers for type errors.
check-types: $(shell ls -d * | grep "openfisca_")
	@printf "${WORKING} Running static type checkers..."
	@mypy $? &> /tmp/result; echo $$? > /tmp/status;
	@[ $$(</tmp/status) -eq 0 ] \
		&& echo ${OK} \
		|| echo "${KO}\n$$(</tmp/result)" \
		&& exit $$(</tmp/status)

## Run code formatters to correct style errors.
format-style: $(shell git ls-files | grep "\.py$$")
	@## Do not analyse .gitignored files.
	@## `make` needs `$$` to output `$`.
	@## See http://stackoverflow.com/questions/2382764.
	@printf "${WORKING} Running code formatters..."
	@autopep8 $?
	@echo ${OK}

# ## Run openfisca-core & country/extension template tests.
test:: clean check-syntax-errors check-style check-types
	@##	Usage:
	@##
	@##		make test [pytest_args="--ARG"] [openfisca_args="--ARG"]
	@##
	@##	Examples:
	@##
	@##		make test
	@##		make test pytest_args="--exitfirst"
	@##		make test openfisca_args="--performance"
	@##		make test pytest_args="--exitfirst" openfisca_args="--performance"

test::
	@echo "${WORKING} Running openfisca-core tests..."
	@[ ! -z "${pytest_args}" ] && echo "${OPTIONS} pytest arguments: ${pytest_args}" ; :
	@PYTEST_ADDOPTS="$$PYTEST_ADDOPTS ${pytest_args}" pytest

test::
	@echo "${WORKING} Running country-template tests..."
	@[ ! -z "${pytest_args}" ] && echo "${OPTIONS} pytest arguments: ${pytest_args}" ; :
	@[ ! -z "${openfisca_args}" ] && echo "${OPTIONS} openfisca arguments: ${openfisca_args}" ; :
	@PYTEST_ADDOPTS="$$PYTEST_ADDOPTS ${pytest_args}" openfisca test ${COUNTRY_TEMPLATE_TESTS} --country-package ${COUNTRY_TEMPLATE} ${openfisca_args}

test::
	@echo "${WORKING} Running extension-template tests..."
	@[ ! -z "${pytest_args}" ] && echo "${OPTIONS} pytest arguments: ${pytest_args}" ; :
	@[ ! -z "${openfisca_args}" ] && echo "${OPTIONS} openfisca arguments: ${openfisca_args}" ; :
	@PYTEST_ADDOPTS="$$PYTEST_ADDOPTS ${pytest_args}" openfisca test ${EXTENSION_TEMPLATE_TESTS} --country-package ${COUNTRY_TEMPLATE} --extensions ${EXTENSION_TEMPLATE} ${openfisca_args}

## Serve the OpenFisca Web API.
serve:
	@##	Usage:
	@##
	@##		make serve [gunicorn_args="--ARG"] [openfisca_args="--ARG"]
	@##
	@##	Examples:
	@##
	@##		make serve
	@##		make serve gunicorn_args="--workers 1"
	@##		make serve openfisca_args="--welcome-message 'Hola :)'"
	@##		make serve gunicorn_args="--workers 1" openfisca_args="--welcome-message 'Hola :)'"
	@echo "${WORKING} Serving the OpenFisca Web API..."
	@[ ! -z "${gunicorn_args}" ] && echo "${OPTIONS} gunicorn arguments: ${gunicorn_args}" ; :
	@[ ! -z "${openfisca_args}" ] && echo "${OPTIONS} openfisca arguments: ${openfisca_args}" ; :
	@openfisca serve --country-package ${COUNTRY_TEMPLATE} --extensions ${EXTENSION_TEMPLATE} ${gunicorn_args} ${openfisca_args}

api:
	@echo $(call WARNINGS, "[make api]\'s been deprecated... please use [make serve] instead!")
	@$(MAKE) serve
