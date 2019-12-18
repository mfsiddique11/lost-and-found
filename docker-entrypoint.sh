#!/usr/bin/env bash
python manage.py db migrate
python manage.py db upgrade
python run.py

