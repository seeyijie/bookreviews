#!/bin/bash
ssh-keygen -R 3.136.18.182
ssh-keyscan -t ecdsa -H 3.136.18.182 >> ~/.ssh/known_hosts