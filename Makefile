SHELL := /bin/bash

# Start the API server
s:
	source ./venv/bin/activate && python santa/server.py

# Start the API server in production mode
sp:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings_prod.py python santa/server.py

# Start the API server using gunicorn
sg:
	source ./venv/bin/activate && gunicorn -c gunicorn.conf.py santa.server:app

# Start the API server using gunicorn in production mode
sgp:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings_prod.py gunicorn -c gunicorn.conf.py santa.server:app

# Start the API server using gunicorn monitored by supervisor
sgs:
	source ./venv/bin/activate && supervisord -c supervisord.conf

# Start the API server using gunicorn monitored by supervisor in production mode
sgsp:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings_prod.py supervisord -c supervisord.conf

# Start the shell
shell:
	source ./venv/bin/activate && python santa/manage.py shell

# Tests
test:
	source ./venv/bin/activate && nose2 -c setup.cfg -v && flake8 .

shippable-test:
	nose2 -c setup.cfg -v && flake8 .
