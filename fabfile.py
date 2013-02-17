#!/usr/bin/env python

from fabric.api import env, run, task, cd, lcd, local, prefix, execute, settings
from fabric.tasks import WrappedCallableTask
from fabric.utils import error
from contextlib import contextmanager as _contextmanager
from sys import executable as sys_executable
from json import load as json_load
from functools import partial

@_contextmanager
def virtualenv():
    with env.cd(env.directory):
        with prefix(env.activate):
            yield

@_contextmanager
def umask(new_mask):
    with prefix('umask %s' % (new_mask, )):
        yield

@_contextmanager
def custom_cd(cdfunction, mask, path):
    with umask(mask):
        with cdfunction(path):
            yield

class CustomTask(WrappedCallableTask):
    def __init__(self, callable, *args, **kwargs):
        super(CustomTask, self).__init__(callable, *args, **kwargs)
        env.use_ssh_config = True
        if env.host_string == 'localhost' or not env.hosts:
            env.pyexecutable = sys_executable
            env.cd = partial(custom_cd, lcd, 002)
            env.run = local
            conffile = 'devenv.json'
        else:
            env.cd = partial(custom_cd, cd, 002)
            env.run = run
            if 'production' in env and env.production:
                error('TBD')
            else:
                conffile = 'testenv.json'

        if 'conffile' in env:
            conffile = env.conffile

        with open(conffile) as f:
            d = json_load(f)

        env.update(d)

        env.activate = ''.join(['. ', env.venvpath, '/bin/activate'])

@task(task_class=CustomTask)
def make_venv():
    with env.cd(env.directory):
        env.run('virtualenv --system-site-packages -p %s %s' % (env.pyexecutable, env.venvpath))

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
        with settings(warn_only=True):
            env.run('python manage.py schemamigration %s --auto' % env.app)
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

@task(task_class=CustomTask)
def rebuild_venv():
    run('rm -rf %s' % (env.venvpath, ))
    execute(update)
    execute(make_venv)
    execute(install_req)
