# Setting up Server Environment

The following sections should walk you through all the steps from creating a DigitalOcean droplet to deploying Santa.

## Create a DigitalOcean droplet

We host the Santa app (staging and production) on [DigitalOcean](https://www.digitalocean.com/). The server is running Ubuntu 14.04 x64.

## Create a takoman user with sudo privilege

Use the root account and create a `takoman` user.

```bash
$ adduser takoman
$ sudo update-alternatives --config editor  # set default editor
$ visudo  # and add takoman to the list
```

After this point, you should be able to just use `takoman` user throughout the steps.

## (Optional) Set up SSH login

In order to log in to the server and use fabtools to deploy without typing password, we can add our local public key to the server's authorized keys:

On your local:
```bash
$ cat ~/.ssh/id_rsa.pub | ssh takoman@api.takoman.co "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"  # Replace the key, username and hostname with correct ones
```

On your local, edit `~/.ssh/config`:
```
Host api.takoman.co
  User takoman
  IdentityFile ~/.ssh/id_rsa
```

Also, you can further [disable the password for root login](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2)

## Set up git

Install
```bash
$ sudo apt-get update
$ sudo apt-get install build-essential
$ sudo apt-get install git
```

Set up git
https://help.github.com/articles/set-up-git

Generate SSH Keys for github
https://help.github.com/articles/generating-ssh-keys#platform-linux

## Set up requirements and install Santa

Please follow the getting started doc for more details.

Install MongoDB

Install Python
```bash
$ sudo apt-get install python-dev
$ sudo apt-get install python-pip
```

Install virtualenv
```bash
$ sudo pip install virtualenv
```

Clone Santa
```bash
$ git clone git@github.com:takoman/santa.git
```

Bootstrap Santa
```bash
$ cd santa
$ make bootstrap
```

Create config files for your environment (staging or production)

## Set up Nginx

Install
```bash
$ sudo apt-get install nginx
```

Add and enable site
```bash
$ sudo vim /etc/nginx/sites-available/api.takoman.co
```

Set up Nginx proxy. See the [Flask docs](http://flask.pocoo.org/docs/deploying/wsgi-standalone/#proxy-setups)

```
server {
    listen 80;

    server_name _;

    access_log  /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log;

    location / {
        proxy_pass         http://127.0.0.1:6000/;
        proxy_redirect     off;

        proxy_set_header   Host             $host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
    }
}
```

```bash
$ sudo ln -s /etc/nginx/sites-available/api.takoman.co /etc/nginx/sites-enabled/api.takoman.co
$ sudo rm /etc/nginx/sites-enabled/default  # To prevent conflict
$ sudo service nginx restart
```
