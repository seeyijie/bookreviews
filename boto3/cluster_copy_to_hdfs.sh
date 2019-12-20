#!/bin/bash
bash cluster_copy_file.sh $1
flintrock run-command my-cluster \
--ec2-user ec2-user \
--ec2-identity-file /home/dominic/.ssh/keypair_wTa33iJQtOBkRZmiFwyecn8yca8FPty3.pem \
'sleep 1 && hadoop fs -put' $1 / && sleep 1