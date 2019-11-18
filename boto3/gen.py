# test to generate configuration files from python scripts
ip = "10.0.0.1"
key = "50043-keypair"

with open ('../scripts/server_scripts/config/run.sh', 'w') as rsh:
    rsh.write(
f'''#!/bin/bash
server_ip="{ip}"
public_key="{key}"''')
