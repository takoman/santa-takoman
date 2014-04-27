# Start the api
s:
	source ./venv/bin/activate && python run.py

sp:
	source ./venv/bin/activate && export EVE_SETTINGS=$(shell pwd)/config/settings.prod.py && python run.py

gsp:
	source ./venv/bin/activate && export EVE_SETTINGS=$(shell pwd)/config/settings.prod.py && gunicorn -c gunicorn.conf.py run:app

# Tests
test:
	source ./venv/bin/activate && export EVE_SETTINGS=$(shell pwd)/config/settings.test.py && nosetests -v $(shell find tests -name '*.py' ! -name '__init__.py')
