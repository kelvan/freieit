#!/usr/bin/env python

from fabric.api import *
from contextlib import contextmanager as _contextmanager
from sys import executable as sys_executable

@_contextmanager
def virtualenv():
    with env.cd(env.directory):
        with prefix(env.activate):
            yield

if not env.hosts:
    raise Exception('no hosts defined')

def prep():
    if env.host_string == 'localhost':
        env.directory = '.'
        env.activate = '. env/bin/activate'
        env.pyexecutable = sys_executable
        env.cd = lcd
        env.run = local
    else:
        #env.hosts = ['freie.it']
        env.directory = 'freieit'
        env.user = 'kelvan'
        env.deploy_user = 'kelvan'
        env.activate = '. /home/kelvan/.virtualenvs/freieit/bin/activate'
        env.cd = cd
        env.pyexecutable = 'python'

def make_venv():
    prep()
    with env.cd(env.directory):
        env.run('virtualenv --system-site-packages -p %s env' % (env.pyexecutable, ))

def vars():
    env.app = 'freieit'

def install_req():
    prep()
    with virtualenv():
        env.run('pip install -U -r requirements.txt')

def runserver():
    prep()
    with virtualenv():
        env.run('python manage.py runserver')

def syncdb():
    prep()
    with virtualenv():
        env.run('python manage.py syncdb')
        env.run('python manage.py migrate freieit')

def clean():
    prep()
    with env.cd(env.directory):
        env.run('rm -f _freieit.db')
        env.run('rm -rf _media/')

def fixtures():
    prep()
    print ExpertProfile.objects.all()[0]

def prepare_migration():
    prep()
    with virtualenv():
        vars()
        env.warn_only = True
        env.run('python manage.py schemamigration %s --auto' % env.app)
        env.warn_only = False
        env.run('hg add %s/migrations' % env.app)

def update():
    prep()
    with env.cd(env.directory):
        env.run('hg pull')
        env.run('hg update')

def deploy():
    prep()
    update()
    with virtualenv():
        env.run('python manage.py syncdb --noinput')
        env.run('python manage.py migrate freieit')

def shell():
    prep()
    with virtualenv():
        env.run('python manage.py shell')

def test_venv():
    prep()
    with virtualenv():
        env.run('python -c "import sys; print sys.path"')
