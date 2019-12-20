#!/bin/bash
flintrock copy-file --assume-yes my-cluster $1 /home/ec2-user/$1 \
--ec2-user ec2-user \
--ec2-identity-file /home/dominic/.ssh/keypair_wTa33iJQtOBkRZmiFwyecn8yca8FPty3.pem \