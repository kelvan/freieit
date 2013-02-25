=========
 fabric file for freie.it webapp
=========

----------------------------------------
manage/deploy freie.it webapp
----------------------------------------

:Author: Albert Dengg <albert@fsfe.org>
:Date: 2013-02-24
:Manual Section: 1

SYNOPSIS
=========

``fab`` [-H hostname] [-A] [--set=KEY=VALUE] [additinonal options] command



DESCRIPTION
===========

  -A                    ssh agent forwarding, needed to to run mercurial commands
                        on the remote host

  -H hostname           hostname/ssh_config entry of the remote host, defaults to
                        localhost.

 --set=KEY=VALUE        set key/value pairs for the internal config. For future use
                        for example production=True to deploy to production instance
                        instead of test instance

 additinonal options    see ``fab --help``

 command                see section ``commands``

COMMANDS
========

clean                   remove development db & media files

collectstatic           merge all static file sources into the target static folder

deploy                  update code & db to current revision

fixtures                load testdata

install_req             install/update requirements in the virtualenv

make_venv               build virtualenv

prepare_migration       ???

rebuild_venv            remove & completly rebuild virtualenv with current requierements

runserver               run django server

shell                   get a shell to the instance


syncdb                  update db

update                  update files

