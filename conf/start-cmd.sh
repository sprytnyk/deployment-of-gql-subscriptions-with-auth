#!/usr/bin/env sh

python manage.py migrate
python manage.py loaddata users.json cars.json

supervisord -c ./conf/supervisor.conf
