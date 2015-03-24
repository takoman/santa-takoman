# Deployment

## Deployment Tools

We use [Fabric](http://www.fabfile.org/) for streamlining the deployment
process from local to remote environments (e.g. staging and production.)
After setting up [SSH config files](http://docs.fabfile.org/en/1.10/usage/execution.html#leveraging-native-ssh-config-files)
on both your local and server, you should be able to deploy Santa to
different environments.
```
fab staging deploy
fab production deploy
```

See the [fabfile](https://github.com/takoman/santa/blob/master/fabfile.py) for more details.

## Deployment Overview

What will happen on the remote server after you run `fab <env> deploy`?

1. Pull the latest master from the [Github repo](https://github.com/takoman/santa).
2. Bootstrap Santa and install requirements.
3. Export remote `.env` (make sure you have modified the .env file on the remote server) to Supervisor config with the [template](https://github.com/takoman/santa/blob/master/supervisord/supervisord-templates/app.conf.erb) (why not just use the Supervisor config file for environment variables? Because we want to use similar .env approach for environment variables as in development.)
4. Update Supervisor configs and environment variables with the newly generated config file and restart Santa app.
5. [Supervisor](http://supervisord.org/) starts managing [Gunicorn](http://flask.pocoo.org/docs/0.10/deploying/wsgi-standalone/#gunicorn) web server processes which run our Santa Flask app.

## Process Management
TODO
