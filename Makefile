VENV = ${VIRTUAL_ENV}

version_file := VERSION
VERSION := $(shell cat ${version_file})

run:
	docker run -i -t --rm --name=archive-manager archive-manager:${VERSION} /bin/bash

image:
	docker build -t archive-manager:${VERSION} . 

test:
	/usr/bin/env python archive_manager/test_archive_manager.py
	# python setup.py tests

rpm:
	# NOTE: this is not currently working as the RPM picks up the virtual env python location
	python setup.py bdist_rpm

coverage:
	coverage run ${VIRTUAL_ENV}/bin/archive-manager -c ${PWD}/config.yml.example -v
	coverage report

pypi:
	python setup.py sdist
	#pip install twine
	twine upload dist/archive-manager-${VERSION}.tar.gz

release:
	# TBD
	# run tests
	# tag? upload to pypi?

cloc:
	cloc .