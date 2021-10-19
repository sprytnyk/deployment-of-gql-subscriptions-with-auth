#!/usr/bin/env python3
import os
import pathlib
import secrets
import sys

import django

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent
sys.path.append(PROJECT_ROOT)
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from app.models import Car

make_choices = ['Skoda', 'Skoda Autogroup', 'Skoda (VAG)']
car = Car.objects.get(pk=1)
car.make = secrets.choice(make_choices)
car.save()
