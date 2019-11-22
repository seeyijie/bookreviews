#!/bin/bash
python3 launch_all.py --image=ami-0d5d9d301c853a04a --keyname=50043-keypair # runs instance and loads
./config_files/fingerprint_mongodb.sh

# run deployment scripts