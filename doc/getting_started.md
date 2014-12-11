# Getting Started with Santa

*Santa* is the codename for the web API at Takoman.

This doc will assume you've set up common development tools.

## Flask

[Flask](http://flask.pocoo.org/) is a Python microframework for building web applications. It is easy and powerful and allows us to build a RESTful API service quickly.

## Development

### Install and run MongoDB

 - Install [MongoDB](http://docs.mongodb.org/manual/installation/)
 - Run [MongoDB](http://docs.mongodb.org/manual/tutorial/manage-mongodb-processes/)

### Install Python and Python-dev
 - Install Python
 - Install Python-dev (needed to compile bcrypt)

   On Ubuntu:
   ```bash
   sudo apt-get install python-dev
   ```

### Install Santa
 - Install pip

   On Ubuntu:
   ```bash
   sudo apt-get install python-pip
   ```
   See the [doc](http://pip.readthedocs.org/en/latest/installing.html) for installation on other platforms.

 - Install virtualenv

   ```bash
   sudo pip install virtualenv
   ```

 - Run bootstrap.sh

   ```bash
   sh bootstrap.sh
   ```

### Run Santa
```bash
make s
```

### Run tests
```bash
make test
```
