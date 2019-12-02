#!/bin/bash
cd /home/ubuntu/bookreviews
source env/bin/activate
sudo nohup gunicorn --bind 0.0.0.0:5000 wsgi:app &