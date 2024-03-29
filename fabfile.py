from __future__ import with_statement
from fabric.api import *

env.use_ssh_config = True  # use local ssh_config

def staging():
    env.hosts = ['api-staging.takoman.co']

def production():
    env.hosts = ['api.takoman.co']

def deploy():
    code_dir = '/home/takoman/santa'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git@github.com:takoman/santa.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("make bootstrap")
        run("make ssp")
