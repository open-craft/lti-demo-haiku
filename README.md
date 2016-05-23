LTI Haiku
=========

Prerequisites
-------------

* python-dev
* virtualenv

Setting up the development server
---------------------------------

1. Install python dependencies

  ```bash
virtualenv .virtualenv
. .virtualenv/bin/activate
pip install -r requirements/base.txt
```

1. Create `app/local_settings.py`, and set the sensitive settings.

  ```python
SECRET_KEY = 'SET ME'
LTI_CLIENT_KEY = 'SET ME'
LTI_CLIENT_SECRET = 'SET ME'
PASSWORD_GENERATOR_NONCE = 'SET ME'

# Optional - can use default sqlite for dev
HAIKU_DB_PASSWORD = 'SET ME'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lti_haiku',
        'USER': 'lti_haiku',
        'PASSWORD': HAIKU_DB_PASSWORD,
    }
}
```

  You can use the following script to generate secret keys:

  ```python
#!/usr/bin/env python
import string
from django.utils.crypto import get_random_string
get_random_string(64, string.hexdigits)
```

1. Initialize app: install dependencies, database, static files, and create a superuser.

  ```bash
./manage.py migrate
./manage.py createsuperuser
```

1. Run server

  ```bash
# Use port 8080 to avoid conflicting with LMS/CMS ports
./manage.py runserver 8080
```

1. Run tests, and view coverage report

  ```bash
pip install -r requirements/test.txt
coverage run --source=. manage.py test
coverage report -m
```
