# Mahila Pratinidhi

## Files
`django-source-code.zip` Django Source Code
`media.zip` Media files zipped ( pictures, profiles)
`postgresql_db.psql` Postgresql Database Dump

## Requirements

Project Framework: `Django (Python 3.5.2)`

Project Dependencies : `./MahilaPratinidhi-production/mahila_pratinidhi/requirements.txt`

Database: `psql (PostgreSQL) 9.5.24`

## Setup

### Extract zip contents
 You should have files `django-source-code.zip` , `media.zip` & `postgresql_db.psql`.
 Extract project source code as well.
 
### Setup python

Install python version  `3.5.2` from package repository.

### Install python venv and pip

Setup python venv and create a virtual environment. See help [here](https://docs.python.org/3/library/venv.html) & [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

### Activate venv and install python dependencies
```
$ python3 venv/bin/activate
$ pip3 install -r requirements.txt
```
### Setup postgresql server

Install postgresql version `9.5.24` server from postgresql repository. See [here](https://www.postgresql.org/download/).

#### Create Posgresql user & database.
Sample example:
```
sudo su - postgres
$ psql
psql> CREATE DATABASE myproject;
psql> CREATE USER myprojectuser WITH PASSWORD 'password';
psql> GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
```

### Create local_settings.py

Copy `/MahilaPratinidhi-production/mahila_pratinidhi/mahila_pratinidhi/local_settings_sample.py` to create new `local_settings.py` file. You should write your custom config in this file.
```
cp ./MahilaPratinidhi-production/mahila_pratinidhi/mahila_pratinidhi/local_settings_sample.py ./MahilaPratinidhi-production/mahila_pratinidhi/mahila_pratinidhi/local_settings.py
```

### Update local_settings.py

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}
```

Update `local_settings.py` with Database `NAME`, `USER`, `PASSWORD`, `HOST`, `PORT`.

`HOST` & `PORT` is where your postgresql server is running.

Add entry to `ALLOWED_HOSTS = ['mahilapratinidhi.naxa.com.np', 'mahilapratinidhi.com']` if you plan to allow other domains/subdomains or ip-address.

Change your `SECRET_KEY` as well.

> 
> You might need to add your `webserver` IP address  to ALLOWED_HOSTS as well.
{.is-warning}


### Restore postgresql dump file

Un-dump the postgresql dump file ie `postgresql_db.psql` to your new database.


### Unzip media.zip

unzip `media.zip` to your `.//MahilaPratinidhi-production/mahila_pratinidhi/` directory so that there everything is withing `media` directory.


### Run the project ( activate venv first)

```
$ cd ./MahilaPratinidhi-production/mahila_pratinidhi/
$ python3 manage.py migrate
$ python3 manage.py collectstatic
$ python3 <path to your venv>/mahilaPratinidhi/bin/gunicorn -c gunicorn_config.py mahila_pratinidhi.wsgi
```

Django server should be now binded to `0.0.0.0:4113`.

### Expose this using Nginx or Other loadbalancer.

`Public` ---> `Nginx` ----> `Django`
