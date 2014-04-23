import os

def numCPUs():
  if not hasattr(os, "sysconf"):
    raise RuntimeError("No sysconf detected.")
  return os.sysconf("SC_NPROCESSORS_ONLN")

def get_log_dir():
  log_dir = pwd + "/log"
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  return log_dir

pwd       = os.getcwd()
log_dir   = get_log_dir()

bind      = "localhost:5000"
workers   = numCPUs() * 2 + 1
backlog   = 2048
daemon    = True
#pidfile   = log_dir + "/gunicorn.pid"
accesslog = log_dir + "/access.log"
errorlog  = log_dir + "/error.log"
#worker_class =  "gevent"
