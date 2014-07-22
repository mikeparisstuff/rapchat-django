from fabric.api import *
from fabric.contrib.console import confirm

env.use_ssh_config = True
env.hosts = ['rapback_web']

def test():
    with settings(warn_only=True):
        result = local('python manage.py test rapback')
    if result.failed and not confirm("Test failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit(message):
    local('''git add -p && git commit -m %s''' % message)

def push():
    local('git push origin')

def merge_to_master(branch_name):
    local('git checkout master && git merge ' + branch_name)

def prepare_deploy(message):
    print message
    commit(message)
    push()

def deploy():
    code_dir = "~/rapback"
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git@github.com:mlp5ab/rapchat-django.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("workon rapback")
        run("pip install -r requirements.txt")
        run("touch app.wsgi")

def run_debug():
    code_dir = "~/rapback"
    with cd(code_dir):
        run("python manage.py runserver 0.0.0.0:8000")
