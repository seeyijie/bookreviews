#!/bin/bash
flintrock run-command my-cluster \
--ec2-user ec2-user \
--ec2-identity-file /home/dominic/.ssh/keypair_wTa33iJQtOBkRZmiFwyecn8yca8FPty3.pem \
-- $1