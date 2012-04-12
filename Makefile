

SHELL = /bin/sh
PYTHON = /usr/bin/env python2.7

MANAGE_SCRIPT = $(PYTHON) manage.py



all: syncdb copy_templates

run:
	$(MANAGE_SCRIPT) runserver

syncdb:
	$(MANAGE_SCRIPT) syncdb #--noinput

create_media_dir:
	mkdir /tmp/freieit_media

copy_templates: clean-templates
	cp -r templates /tmp/freieit_templates

.PHONY: clean clean-db clean-media clean-static

clean: clean-db clean-media clean-static clean-templates clean-media-dir

clean-db:
	rm -f /tmp/freieit.db

clean-media:
	rm -rf /tmp/freieit_media

clean-static:
	rm -rf /tmp/freieit_static

clean-templates:
	rm -rf /tmp/freieit_templates

clean-media-dir:
	rm -rf /tmp/freieit_media
