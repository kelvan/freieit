

SHELL = /bin/sh
PYTHON = /usr/bin/env python2.7

MANAGE_SCRIPT = $(PYTHON) manage.py



all: fixtures

run:
	$(MANAGE_SCRIPT) runserver

syncdb:
	$(MANAGE_SCRIPT) syncdb --noinput

fixtures: fixtures-db fixtures-media

fixtures-db: syncdb
	$(MANAGE_SCRIPT) loaddata dev-fixtures/fixture.json

fixtures-media: clean-media
	cp -r dev-fixtures/media ./_media

.PHONY: clean clean-db

clean: clean-db clean-media

clean-db:
	rm -f _freieit.db

clean-media:
	rm -rf _media

clean-fixtures: clean-db clean-media
