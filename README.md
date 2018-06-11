[![Build](https://travis-ci.org/power-analyzer/backend.svg?branch=master)](https://travis-ci.org/power-analyzer/backend?branch=master)


# Power Analyzer (Backend)
This is the backend component of Nathan Zimmerly and Ryan Rabello's senior
project.

## Requirements
- Django v2.0

## Run The Server

1. Install Requirements

  ```
  pip install -r requirements.txt
  ```
2. Run Server
  ```
  python manage.py runserver
  ```

## Add or remove data (via django admin)

  1. If you haven't already creat a super user
  ```
  python manage.py createsuperuser
  ```

  2. Go to [localhost:8000/admin](http://localhost:8000/admin) and Login with
  the credentials you just created.

  3. Have fun viewing & editing the data.
