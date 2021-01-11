#!/bin/sh
gunicorn -b 0.0.0.0:50005 --worker-class eventlet -w 1 main:app