from fabric.api import local

env.hosts = ['']

def uptime():
    local('uptime')

