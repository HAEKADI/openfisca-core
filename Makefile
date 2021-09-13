info = $$(tput setaf 6)[i]$$(tput sgr0)
warn = $$(tput setaf 3)[!]$$(tput sgr0)
work = $$(tput setaf 5)[⚙]$$(tput sgr0)
pass = echo $$(tput setaf 2)[✓]$$(tput sgr0) Good work! =\> $$(tput setaf 8)$1$$(tput sgr0)$$(tput setaf 2)passed$$(tput sgr0) 🚀
help = sed -n "/^$1/ { x ; p ; } ; s/\#\#/$(work)/ ; s/\./.../ ; x" ${MAKEFILE_LIST}
repo = https://github.com/openfisca/openfisca-doc
branch = $(shell git branch --show-current)

## Same as `make test`.
all: test

## Install project dependencies.
install:
	@$(call help,$@:)
	@pip install --upgrade pip twine wheel
	@pip install --editable .[dev] --upgrade --use-deprecated=legacy-resolver

## Install openfisca-core for deployment and publishing.
build: setup.py
	@## This allows us to be sure tests are run against the packaged version
	@## of openfisca-core, the same we put in the hands of users and reusers.
	@$(call help,$@:)
	@python $? bdist_wheel
	@find dist -name "*.whl" -exec pip install --force-reinstall {}[dev] \;

## Uninstall project dependencies.
uninstall:
	@$(call help,$@:)
	@pip freeze | grep -v "^-e" | sed "s/@.*//" | xargs pip uninstall -y

## Delete builds and compiled python files.
clean: \
	$(shell ls -d * | grep "build\|dist") \
	$(shell find . -name "*.pyc")
	@$(call help,$@:)
	@rm -rf $?

## Compile python files to check for syntax errors.
check-syntax-errors: .
	@$(call help,$@:)
	@python -m compileall -q $?

## Run linters to check for syntax and style errors.
check-style: $(shell git ls-files "*.py")
	@$(call help,$@:)
	@flake8 $?

	@# Check that docstrings are present in public class, method, and function definitions.
	@# See: http://www.pydocstyle.org/en/2.1.1/error_codes.html
	@flake8 --select=D101,D102,D103 openfisca_core/commons

	@# Check that docstrings match the current implementation of functions/methods.
	@# See: https://github.com/terrencepreilly/darglint
	@flake8 --select=DAR openfisca_core/commons

	@# Further check for syntax and design errors —style excluded.
	@# See: `pylint --list-msgs`
	@pylint --enable=classes,exceptions,imports,miscellaneous,refactoring --disable=W0201,W0231 openfisca_core/commons

## Run static type checkers for type errors.
check-types: openfisca_core openfisca_web_api
	@$(call help,$@:)
	@mypy $?

## Run code formatters to correct style errors.
format-style: $(shell git ls-files "*.py")
	@$(call help,$@:)
	@autopep8 $?

## Run openfisca-core tests.
test: clean check-syntax-errors check-style check-types
	@$(call help,$@:)
	@PYTEST_ADDOPTS="${PYTEST_ADDOPTS}" pytest --cov=openfisca_core --cov=openfisca_web_api

## Check that the current changes do not break the doc.
test-doc:
	@##	Usage:
	@##
	@##		make test-doc [branch=BRANCH]
	@##
	@##	Examples:
	@##
	@##		# Will check the current branch in openfisca-doc.
	@##		make test-doc
	@##
	@##		# Will check "test-doc" in openfisca-doc.
	@##		make test-doc branch=test-doc
	@##
	@##		# Will check "master" if "asdf1234" does not exist.
	@##		make test-doc branch=asdf1234
	@##
	@$(call help,$@:)
	@${MAKE} test-doc-checkout
	@${MAKE} test-doc-install
	@${MAKE} test-doc-build
	@$(call pass,$@:)

## Update the local copy of the doc.
test-doc-checkout:
	@$(call help,$@:)
	@[ ! -d doc ] && git clone ${repo} doc || :
	@cd doc && { \
		git reset --hard ; \
		git fetch --all ; \
		[ "$$(git branch --show-current)" != "master" ] && git checkout master || : ; \
		[ "${branch}" != "master" ] \
			&& { \
				{ \
					>&2 echo "$(info) Trying to checkout the branch 'openfisca-doc/${branch}'..." ; \
					git branch -D ${branch} 2> /dev/null ; \
					git checkout ${branch} 2> /dev/null ; \
				} \
					&& git pull --ff-only origin ${branch} \
					|| { \
						>&2 echo "$(warn) The branch 'openfisca-doc/${branch}' was not found, falling back to 'openfisca-doc/master'..." ; \
						>&2 echo "" ; \
						>&2 echo "$(info) This is perfectly normal, one of two things can ensue:" ; \
						>&2 echo "$(info)" ; \
						>&2 echo "$(info) $$(tput setaf 2)[If tests pass]$$(tput sgr0)" ; \
						>&2 echo "$(info)     * No further action required on your side..." ; \
						>&2 echo "$(info)" ; \
						>&2 echo "$(info) $$(tput setaf 1)[If tests fail]$$(tput sgr0)" ; \
						>&2 echo "$(info)     * Create the branch '${branch}' in 'openfisca-doc'... " ; \
						>&2 echo "$(info)     * Push your fixes..." ; \
						>&2 echo "$(info)     * Run 'make test-doc' again..." ; \
						>&2 echo "" ; \
						>&2 echo "$(work) Checking out 'openfisca-doc/master'..." ; \
						git pull --ff-only origin master ; \
					} \
			} \
			|| git pull --ff-only origin master ; \
	} 1> /dev/null

## Install doc dependencies.
test-doc-install:
	@$(call help,$@:)
	@pip install --requirement doc/requirements.txt 1> /dev/null
	@pip install --editable .[dev] --upgrade 1> /dev/null

## Dry-build the doc.
test-doc-build:
	@$(call help,$@:)
	@sphinx-build -M dummy doc/source doc/build -n -q -W

## Serve the openfisca Web API.
api:
	@$(call help,$@:)
	@openfisca serve \
		--country-package openfisca_country_template \
		--extensions openfisca_extension_template
