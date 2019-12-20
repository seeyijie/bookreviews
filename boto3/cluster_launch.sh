#!/bin/bash
flintrock launch my-cluster \
--install-hdfs \
--hdfs-version 2.8.5 \
--install-spark \
--spark-version 2.4.4 \
--ec2-user ec2-user \
--ec2-instance-profile-name EMR_EC2_DefaultRole \
--ec2-key-name keypair_wTa33iJQtOBkRZmiFwyecn8yca8FPty3 \
--ec2-region us-east-1 \
--ec2-identity-file /home/dominic/.ssh/keypair_wTa33iJQtOBkRZmiFwyecn8yca8FPty3.pem \
--ec2-instance-type t3.large \
--ec2-ami ami-00068cd7555f543d5 \
--num-slaves 3 \