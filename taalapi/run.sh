#!/bin/bash

python3 manage.py migrate

exec uwsgi --ini uwsgi.ini
