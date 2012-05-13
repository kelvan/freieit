

SHELL = /bin/sh
PYTHON = /usr/bin/env python2.6

MANAGE_SCRIPT = $(PYTHON) manage.py



all: fixtures

run:
	$(MANAGE_SCRIPT) runserver

#syncdb:
#	$(MANAGE_SCRIPT) syncdb --noinput

fixtures: fixtures-db fixtures-media

fixtures-db:
	#$(MANAGE_SCRIPT) loaddata dev-fixtures/fixture.json
	cp dev-fixtures/freieit.db _freieit.db
	$(MANAGE_SCRIPT) syncdb --noinput

fixtures-media: clean-media
	cp -r dev-fixtures/media ./_media

.PHONY: clean clean-db clean-media clean-fixtures

clean: clean-db clean-media
	rm -f `find . -name '*.pyc'`
	rm -f `find . -name '*.pyo'`

clean-db:
	rm -f _freieit.db

clean-media:
	rm -rf _media

clean-fixtures: clean-db clean-media
