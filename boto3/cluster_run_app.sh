#!/bin/bash
bash cluster_run_command.sh curl -O https://bootstrap.pypa.io/get-pip.py && sudo python get-pip.py && sudo pip install numpy
bash cluster_copy_file.sh $1
flintrock run-command my-cluster 'spark-submit --packages org.apache.hadoop:hadoop-aws:2.7.6' $1 \
--ec2-user ec2-user \
--ec2-identity-file /home/dominic/.ssh/keypair_wTa33iJQtOBkRZmiFwyecn8yca8FPty3.pem \
--master-only \