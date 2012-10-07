from fabric.api import *
from fabric.contrib import django

def production():
    env.hosts = ['freie.it']
    env.directory = 'freieit'
    env.user = 'kelvan'
    env.deploy_user = 'kelvan'
    env.activate = 'source /home/kelvan/.virtualenvs/freieit/bin/activate'

def dev():
    env.directory = '.'
    env.activate = 'source env/bin/activate'

def vars():
    env.app= 'freieit'

def virtualenv(command):
    with cd(env.directory):
        run(env.activate + '&&' + command)

def lvirtualenv(command):
    with lcd(env.directory):
        local(env.activate + '&&' + command)

def pip_install_req():
    virtualenv('pip install -U -r freieit/requirements.txt')

def runserver():
    dev()
    lvirtualenv('python manage.py runserver')

def syncdb():
    lvirtualenv('python manage.py syncdb')
    lvirtualenv('python manage.py migrate freieit')

def prepare_migration():
    dev()
    with lcd(env.directory):
        vars()
        env.warn_only = True
        lvirtualenv('python manage.py schemamigration %s --auto' % env.app)
        env.warn_only = False
        local('hg add %s/migrations' % env.app)

def pull_update():
    with cd(env.directory):
        run('hg pull')
        run('hg update')

def deploy():
    pull_update()
    virtualenv('python manage.py syncdb')
    virtualenv('python manage.py migrate freieit')
