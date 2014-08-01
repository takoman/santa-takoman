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
sgs:
	source ./venv/bin/activate
	# TODO Run supervisord when an instance is already running will error.
	# Let's ignore it for now and will need a better way to check that.
	-supervisord -c supervisord.conf
	supervisorctl -c supervisord.conf start santa:development

# Start the API server in staging mode using gunicorn monitored by supervisor
ssgs:
	source ./venv/bin/activate
	# TODO Run supervisord when an instance is already running will error.
	# Let's ignore it for now and will need a better way to check that.
	-supervisord -c supervisord.conf
	supervisorctl -c supervisord.conf start santa:staging

# Start the API server in production mode using gunicorn monitored by supervisor
spgs:
	source ./venv/bin/activate
	# TODO Run supervisord when an instance is already running will error.
	# Let's ignore it for now and will need a better way to check that.
	-supervisord -c supervisord.conf
	supervisorctl -c supervisord.conf start santa:production

# Start the shell
shell:
	source ./venv/bin/activate && python santa/manage.py shell

# Tests
test:
	source ./venv/bin/activate && nose2 -c setup.cfg -v && flake8 .

shippable-test:
	nose2 -c setup.cfg -v && flake8 .
