# -*- coding: utf-8 -*-

import os, multiprocessing

def available_cpu_count():
    try:
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        raise Exception('Can not determine number of CPUs on this system')

def get_log_dir():
    log_dir = os.getcwd() + "/log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

def bind_address():
    host = os.environ.get('SANTA_HOST', '127.0.0.1')
    port = os.environ.get('SANTA_PORT', '5000')
    return host + ":" + port

log_dir   = get_log_dir()

# Server Socket
bind      = bind_address()
backlog   = 2048

# Worker Processes
workers   = available_cpu_count() * 2 + 1

# Server Mechanics
# Make sure that when using either of these service monitors you do not enable the Gunicorn's daemon mode.
# daemon    = True

# Logging
# accesslog = log_dir + "/access.log"
# errorlog  = log_dir + "/error.log"
loglevel = 'debug'

# Process Naming
proc_name = "santa"
