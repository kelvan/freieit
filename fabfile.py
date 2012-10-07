from fabric.api import *
#from fabric.contrib import django

#django.project('freieit')
#from freieit.models import ExpertProfile

def production():
    env.hosts = ['freie.it']
    env.directory = 'freieit'
    env.user = 'kelvan'
    env.deploy_user = 'kelvan'
    env.activate = '. /home/kelvan/.virtualenvs/freieit/bin/activate'

def dev():
    env.directory = '.'
    env.activate = '. env/bin/activate'

def vars():
    env.app= 'freieit'

def virtualenv(command):
    with cd(env.directory):
        run(env.activate + '&&' + command)

def lvirtualenv(command):
    with lcd(env.directory):
        local(env.activate + '&&' + command)

def make_venv():
    dev()
    with lcd(env.directory):
        local('virtualenv-2.7 -p python2.7 env')

def install_req():
    dev()
    lvirtualenv('pip install -U -r requirements.txt')

def runserver():
    dev()
    lvirtualenv('python manage.py runserver')

def syncdb():
    dev()
    lvirtualenv('python manage.py syncdb')
    lvirtualenv('python manage.py migrate freieit')

def clean():
    dev()
    with lvd(env.directory):
        local('rm -f _freieit.db')
        local('rm -rf _media/')

def fixtures():
    dev()
    print ExpertProfile.objects.all()[0]

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
    virtualenv('python manage.py syncdb --noinput')
    virtualenv('python manage.py migrate freieit')
