SHELL := /bin/bash
LOG_DIR = ./log

# Start the API server
s:
	source ./venv/bin/activate && foreman start

# Start the API server with supervisor
ssp:
	source ./venv/bin/activate; \
	mkdir -p $(LOG_DIR); \
	SUPERVISORD_PID=$$(supervisorctl -c supervisord.conf pid); \
	case $$SUPERVISORD_PID in \
	  ''|*[!0-9]*) echo 'Starting supervisord...'; supervisord -c supervisord.conf ;; \
	  *) echo 'Supervisored is already running.'; \
	esac; \
	SANTA_PID=$$(supervisorctl -c supervisord.conf pid santa:api); \
	case $$SANTA_PID in \
	  0|''|*[!0-9]*) echo 'Starting santa api...'; supervisorctl -c supervisord.conf start santa:api ;; \
	  *) echo 'Reloading santa api...'; kill -HUP $$SANTA_PID; \
	esac; \

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
