#!/bin/bash
bash cluster_launch.sh
bash cluster_install_numpy.sh
bash cluster_copy_file info.txt
bash cluster_run_app.sh spark_app.py