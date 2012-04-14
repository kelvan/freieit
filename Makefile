

SHELL = /bin/sh
PYTHON = /usr/bin/env python2.7

MANAGE_SCRIPT = $(PYTHON) manage.py



all: syncdb

run:
	$(MANAGE_SCRIPT) runserver

syncdb:
	$(MANAGE_SCRIPT) syncdb #--noinput


.PHONY: clean clean-db

clean: clean-db clean-media clean-static

clean-db:
	rm -f freieit.db

clean-media:
	rm -rf _media

clean-static:
	rm -rf _static

