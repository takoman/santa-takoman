SHELL := /bin/bash

# Start the API server
s:
	source ./venv/bin/activate && python santa/server.py

# Start the API server in staging mode
ss:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings_staging.py SANTA_HOST=0.0.0.0 SANTA_PORT=6000 python santa/server.py

# Start the API server in production mode
sp:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings_production.py SANTA_HOST=0.0.0.0 SANTA_PORT=7000 python santa/server.py

# Start the API server using gunicorn
sg:
	source ./venv/bin/activate && gunicorn -c gunicorn.conf.py santa.server:app

# Start the API server in staging mode using gunicorn
ssg:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings_staging.py SANTA_HOST=0.0.0.0 SANTA_PORT=6000 gunicorn -c gunicorn.conf.py santa.server:app

# Start the API server in production mode using gunicorn
spg:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings_production.py SANTA_HOST=0.0.0.0 SANTA_PORT=7000 gunicorn -c gunicorn.conf.py santa.server:app

# Start the API server using gunicorn monitored by supervisor
# Pass the mode in the `env` environment variable, for example,
# 	`env=staging make sgs`      # Run Santa in staging mode
# 	`env=production make sgs`   # Run Santa in production mode
# TODO: Need to check the `env` env var; otherwise, supervisor will start all of them.
sgs:
	source ./venv/bin/activate; \
	SUPERVISORD_PID=$$(supervisorctl -c supervisord.conf pid); \
	case $$SUPERVISORD_PID in \
	  ''|*[!0-9]*) echo 'Starting supervisord...'; supervisord -c supervisord.conf ;; \
	  *) echo 'Supervisored is already running.' ;; \
	esac; \
	SANTA_PID=$$(supervisorctl -c supervisord.conf pid santa:$(env)); \
	case $$SANTA_PID in \
	  0|''|*[!0-9]*) echo 'Starting santa $(env)...'; supervisorctl -c supervisord.conf start santa:$(env) ;; \
	  *) echo 'Reloading santa $(env)...'; kill -HUP $$SANTA_PID ;; \
	esac; \

# Start the shell
shell:
	source ./venv/bin/activate && python santa/manage.py shell

# Tests
test:
	source ./venv/bin/activate && nose2 -c setup.cfg -v && flake8 .

shippable-test:
	nose2 -c setup.cfg -v && flake8 .
