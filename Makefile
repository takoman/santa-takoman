# Start the api
s:
	source ./venv/bin/activate && python run.py

sp:
	source ./venv/bin/activate && EVE_SETTINGS=$(shell pwd)/config/settings.prod.py python run.py

gsp:
	source ./venv/bin/activate && EVE_SETTINGS=$(shell pwd)/config/settings.prod.py gunicorn -c gunicorn.conf.py run:app

# Tests
test:
	source ./venv/bin/activate && EVE_SETTINGS=$(shell pwd)/config/settings.test.py nosetests -c ./.noserc $(shell find tests -name '*.py' ! -name '__init__.py') && flake8 .

shippable-test:
	EVE_SETTINGS=$(shell pwd)/config/settings.test.py nosetests -c ./.noserc $(shell find tests -name '*.py' ! -name '__init__.py') && flake8 .
