
SHELL = /bin/sh

PY_EXISTS = $(shell test -x "/usr/bin/python2.7"; echo $$?)

ifeq ($(PY_EXISTS),0)
    PYTHON=/usr/bin/env python2.7
else
	PYTHON=/usr/bin/env python2.6
endif

MANAGE_SCRIPT=${PYTHON} manage.py

all: fixtures rebuild-index

run:
	$(MANAGE_SCRIPT) runserver

fixtures: fixtures-db fixtures-media

fixtures-db:
	#$(MANAGE_SCRIPT) loaddata dev-fixtures/fixture.json
	cp dev-fixtures/freieit.db _freieit.db
	#$(MANAGE_SCRIPT) syncdb --noinput

fixtures-media: clean-media
	cp -r dev-fixtures/media ./_media

rebuild-index:
	$(MANAGE_SCRIPT) rebuild_index

.PHONY: clean clean-db clean-media clean-fixtures

clean: clean-db clean-media
	rm -f `find . -name '*.pyc'`
	rm -f `find . -name '*.pyo'`

clean-db:
	rm -f _freieit.db

clean-media:
	rm -rf _media

clean-fixtures: clean-db clean-media

#syncdb: conf
#	$(MANAGE_SCRIPT) syncdb --noinput

