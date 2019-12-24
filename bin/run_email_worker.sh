#!/usr/bin/env bash

sleep 10s
celery worker -A app.common.email.celery --loglevel=info
