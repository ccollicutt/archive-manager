VENV = ${VIRTUAL_ENV}

version_file := VERSION
VERSION := $(shell cat ${version_file})

run: image
	docker run -i -t --rm --name=archive-manager archive-manager:${VERSION} /bin/sh

image:
	docker build --build-arg version=${VERSION} -t archive-manager:${VERSION} .

test:
	# python -m unittest discover archive_manager
	/usr/bin/env python archive_manager/test_archive_manager.py
	# python setup.py tests

rpm:
	# NOTE: this is not currently working as the RPM picks up the virtual env python location
	python setup.py bdist_rpm

coverage:
	coverage run ${VIRTUAL_ENV}/bin/archive-manager -c ${PWD}/config.yml.example -v
	coverage report

pypi:
    # FIXME: need some kind of automated release
	# FIXME: need some kind of rc style release?
	# bump version in VERSION file
    # commit current changes
	# push
	# check if tests pass
	# create dist:
	python setup.py sdist
	#pip install twine
	twine upload dist/archive-manager-${VERSION}.tar.gz
	# git tag -a "v0.1.4" -m "new version"
    # git push --tags

release:
	# TBD
	# run tests
	# tag? upload to pypi?

cloc:
	cloc .