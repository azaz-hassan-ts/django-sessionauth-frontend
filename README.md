# djangoauth-2.0-sessionauth

## Deployed at https://sessionauthfrontend.herokuapp.com/

# Python: Getting Started

A barebones Django app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python 3.9 [installed locally](https://docs.python-guide.org/starting/installation/). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/azaz-hassan-ts/djangoauth.git
$ cd djangoauth

$ python3 -m venv getting-started
$ pip install -r requirements.txt

$ createdb django_auth

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku main

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)


## Swagger Documentation Hits


### Got to https://sessionauthfrontend.herokuapp.com/test/ to see swagger spec document
#### Note: Session Auth is integrated in Swagger Spec document
#### API HIT CYCLE:

```
1. Create a user on signup page
2. login, it will start session and show username
3. OPen profile and it will show details
4. logout and profile won't be available now
```

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)


# django-sessionauth-frontend
