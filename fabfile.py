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

@_contextmanager
def shell_env(**ENVS):
    with prefix(' && '.join('export %s=%s' % (k, v) for k,v in ENVS.items())):
        yield

def manage_django(command):
    with virtualenv():
        with shell_env(PYTHONPATH=env['PYTHONPATH']):
            env.run('python manage.py %s --settings=%s' % (command, env.django_settings))

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
    manage_django('runserver')

@task(task_class=CustomTask)
def syncdb():
    manage_django('syncdb')
    manage_django('migrate freieit')

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
    vars()
    with settings(warn_only=True):
        manage_django('schemamigration %s --auto' % env.app)
    env.run('hg add %s/migrations' % env.app)

@task(task_class=CustomTask)
def update():
    with env.cd(env.directory):
        env.run('hg pull')
        env.run('hg update')

@task(task_class=CustomTask)
def deploy():
    execute(update)
    manage_django('syncdb --noinput')
    manage_django('migrate freieit')

@task(task_class=CustomTask)
def shell():
    manage_django('shell')

@task(task_class=CustomTask)
def rebuild_venv():
    env.run('rm -rf %s' % (env.venvpath, ))
    execute(update)
    execute(make_venv)
    execute(install_req)

@task(task_class=CustomTask)
def collectstatic():
    manage_django('collectstatic --noinput')
