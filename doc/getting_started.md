# Getting Started with Santa

*Santa* is the codename for the web API at Takoman.

This doc will assume you've set up common development tools.

## Flask

[Flask](http://flask.pocoo.org/) is a Python microframework for building web applications. It is easy and powerful and allows us to build a RESTful API service quickly.

## Development

#### Install and run MongoDB

 - Install [MongoDB](http://docs.mongodb.org/manual/installation/)
 - Run [MongoDB](http://docs.mongodb.org/manual/tutorial/manage-mongodb-processes/)

#### Install Python and Python-dev
 - Install Python
 - Install Python-dev (needed to compile bcrypt)

   On Ubuntu:
   ```bash
   sudo apt-get install python-dev
   ```

#### Install Santa
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
 
 - Fork/Clone the Santa repository

 - Bootstrap your local Santa

   ```bash
   cd santa
   make bootstrap
   ```

 - Set up environment variables in your local `.env` file for `foreman`.
   ```bash
   cp .env.example .env
   # Modify the environment variables in .env
   ```

#### Run Santa
 - We use [foreman](https://github.com/ddollar/foreman) to manage our app in development. Install foreman if you don't have it on your local.
 - Run the app

   ```bash
   make s
   ```

 - Santa should now be running at http://localhost:5000/

#### Run tests
```bash
make test
```

#### Run shell
```bash
make shell
```
