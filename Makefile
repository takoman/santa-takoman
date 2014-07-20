SHELL := /bin/bash

# Start the api
s:
	source ./venv/bin/activate && python santa/server.py

sp:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings.prod.py python santa/server.py

gs:
	source ./venv/bin/activate && gunicorn -c gunicorn.conf.py santa.server:app

gsp:
	source ./venv/bin/activate && SANTA_SETTINGS=$(shell pwd)/santa/config/settings.prod.py gunicorn -c gunicorn.conf.py santa.server:app

# Start the shell
shell:
	source ./venv/bin/activate && python santa/manage.py shell

# Tests
test:
	source ./venv/bin/activate && nose2 -c setup.cfg -v && flake8 .

shippable-test:
	nose2 -c setup.cfg -v && flake8 .
