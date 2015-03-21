SHELL := /bin/bash
LOG_DIR = log
SUPERVISORD_DIR = supervisord
SUPERVISORD_TEMPLATE_DIR = $(SUPERVISORD_DIR)/supervisord-templates

# Start the API server
s:
	source ./venv/bin/activate && foreman start

# Start the API server with Supervisord.
# Note that `supervisorctl update` will reload the program configs and
# restart the programs (if the programs have autostart=true).
# `start all` just in case `update` does not start the programs.
ssp:
	source ./venv/bin/activate; \
	mkdir -p $(LOG_DIR); \
	foreman export --template $(SUPERVISORD_TEMPLATE_DIR) --app santa --log $(LOG_DIR) supervisord $(SUPERVISORD_DIR); \
	SUPERVISORD_PID=$$(supervisorctl -c $(SUPERVISORD_DIR)/santa.conf pid); \
	case $$SUPERVISORD_PID in \
	  ''|*[!0-9]*) echo 'Starting Supervisord...'; supervisord -c $(SUPERVISORD_DIR)/santa.conf ;; \
	  *) echo 'Supervisord is already running.'; \
	esac; \
	echo 'Reloading Supervisord config and restarting Santa...'; \
	supervisorctl -c $(SUPERVISORD_DIR)/santa.conf update; \
	supervisorctl -c $(SUPERVISORD_DIR)/santa.conf start all; \

# Start the shell
shell:
	source ./venv/bin/activate && foreman run python santa/manage.py shell

# Bootstrap Santa
# Need to export the ARCHFLAGS env var on Mac for Xcode 5.1 compilation fix.
# http://bruteforce.gr/bypassing-clang-error-unknown-argument.html
bootstrap:
	virtualenv venv; \
	export ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future; \
	source ./venv/bin/activate && pip install -r requirements.txt; \
	python setup.py develop; \

# Tests
test:
	source ./venv/bin/activate && nose2 -c setup.cfg -v && flake8 .

shippable-test:
	nose2 -c setup.cfg -v && flake8 .

.PHONY: s ssp shell bootstrap test shippable-test
