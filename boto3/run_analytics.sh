# ================== Phase 3 - Execute analytics tasks and get results ====================
bash cluster_install_numpy.sh
bash cluster_copy_file.sh info.txt
bash cluster_run_app.sh spark_app.py
python3 aws_setup.py import_results_from_bucket