SHELL := /bin/bash

# Start the API server
s:
	source ./venv/bin/activate && python santa/server.py

# Start the API server in staging mode
ss:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings_staging.py python santa/server.py

# Start the API server in production mode
sp:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings_production.py python santa/server.py

# Start the API server using gunicorn
sg:
	source ./venv/bin/activate && gunicorn -c gunicorn.conf.py santa.server:app

# Start the API server using gunicorn in staging mode
sgs:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings_staging.py gunicorn -c gunicorn.conf.py santa.server:app

# Start the API server using gunicorn in production mode
sgp:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings_production.py gunicorn -c gunicorn.conf.py santa.server:app

# Start the API server using gunicorn monitored by supervisor
sgv:
	source ./venv/bin/activate && supervisord -c supervisord.conf

# Start the API server using gunicorn monitored by supervisor in staging mode
sgvs:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings_staging.py supervisord -c supervisord.conf

# Start the API server using gunicorn monitored by supervisor in production mode
sgvp:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings_production.py supervisord -c supervisord.conf

# Start the shell
shell:
	source ./venv/bin/activate && python santa/manage.py shell

# Tests
test:
	source ./venv/bin/activate && nose2 -c setup.cfg -v && flake8 .

shippable-test:
	nose2 -c setup.cfg -v && flake8 .
