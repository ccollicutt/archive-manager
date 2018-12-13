VERSION = 0.1.1
ITERATION = 0
RPM_NAME = archive-manager-${VERSION}-${ITERATION}.x86_64.rpm
VENV = ${VIRTUAL_ENV}
PYTHON=/usr/bin/python

run:
	docker run -i -t --rm --name=archive-manager archive-manager

image: rpm 
	docker build -t archive-manager .

test:
	/usr/bin/env python archive_manager/test_archive_manager.py

rpm:
	# NOTE: this is not currently working as the RPM picks up the virtual env python location
	python setup.py bdist_rpm

coverage:
	coverage run ${VIRTUAL_ENV}/bin/archive-manager -c ${PWD}/config.yml.example -v
	coverage report

cloc:
	cloc .