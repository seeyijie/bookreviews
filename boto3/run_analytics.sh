#!/bin/bash
bash cluster_launch.sh
python finalize_spark_script.py spark_app.py
bash cluster_run_app.sh spark_app.py