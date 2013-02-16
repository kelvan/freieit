#!/usr/bin/env python

from fabric.api import env, run, task, cd, lcd, local, prefix, execute
from fabric.tasks import WrappedCallableTask
from fabric.utils import error
from contextlib import contextmanager as _contextmanager
from sys import executable as sys_executable

@_contextmanager
def virtualenv():
    with env.cd(env.directory):
        with prefix(env.activate):
            yield

class CustomTask(WrappedCallableTask):
    def __init__(self, callable, *args, **kwargs):
        super(CustomTask, self).__init__(callable, *args, **kwargs)
        if env.host_string == 'localhost' or not env.hosts:
            env.directory = '.'
            env.activate = '. env/bin/activate'
            env.pyexecutable = sys_executable
            env.cd = lcd
            env.run = local
        else:
            if env.production:
                error('TBD')
            else:
                env.directory = 'freieit'
                env.user = 'kelvan'
                env.deploy_user = 'kelvan'
                env.activate = '. /home/kelvan/.virtualenvs/freieit/bin/activate'
                env.cd = cd
                env.run = run
                env.pyexecutable = 'python'

@task(task_class=CustomTask)
def make_venv():
    with env.cd(env.directory):
        env.run('virtualenv --system-site-packages -p %s env' % (env.pyexecutable, ))

def vars():
    env.app = 'freieit'

@task(task_class=CustomTask)
def install_req():
    with virtualenv():
        env.run('pip install -U -r requirements.txt')

@task(task_class=CustomTask)
def runserver():
    with virtualenv():
        env.run('python manage.py runserver')

@task(task_class=CustomTask)
def syncdb():
    with virtualenv():
        env.run('python manage.py syncdb')
        env.run('python manage.py migrate freieit')

@task(task_class=CustomTask)
def clean():
    with env.cd(env.directory):
        env.run('rm -f _freieit.db')
        env.run('rm -rf _media/')

@task(task_class=CustomTask)
def fixtures():
    print ExpertProfile.objects.all()[0]

@task(task_class=CustomTask)
def prepare_migration():
    with virtualenv():
        vars()
        env.warn_only = True
        env.run('python manage.py schemamigration %s --auto' % env.app)
        env.warn_only = False
        env.run('hg add %s/migrations' % env.app)

@task(task_class=CustomTask)
def update():
    with env.cd(env.directory):
        env.run('hg pull')
        env.run('hg update')

@task(task_class=CustomTask)
def deploy():
    execute(update)
    with virtualenv():
        env.run('python manage.py syncdb --noinput')
        env.run('python manage.py migrate freieit')

@task(task_class=CustomTask)
def shell():
    with virtualenv():
        env.run('python manage.py shell')

@task(task_class=CustomTask)
def test_venv():
    with virtualenv():
        env.run('python -c "import sys; print sys.path"')
