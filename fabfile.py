from fabric.api import local, settings, abort
from fabric.contrib.console import confirm

def test():
    with settings(warn_only=True):
        result = local('python manage.py test rapback')
    if result.failed and not confirm("Test failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit():
    local('git add -p && git commit')

def push():
    local('git push origin')

def merge_to_master(branch_name):
    local('git checkout master && git merge ' + branch_name)

def prepare_deploy():
    commit()
    push()

def deploy():
    code_dir = "~/rapback"
