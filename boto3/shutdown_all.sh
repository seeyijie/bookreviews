#!/bin/bash
bash cluster_terminate.sh
python3 terminate_backend.py
python3 aws_setup.py delete_bucket