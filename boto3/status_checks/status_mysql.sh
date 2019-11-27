#!/bin/bash
# this script checks if the server has finished executing the user data script
# boot-finished file will be generated upon completion of user data script

# TODO: add strict host checking flag to "no"
status=false

if ssh -o StrictHostKeyChecking=no -i ~/.ssh/50043-keypair.pem ubuntu@18.222.173.254 stat "/var/lib/cloud/instance/boot-finished" \> /dev/null 2\>\&1
            then
                    status=true
                    echo "File exists"
            else
                    status=false
                    echo "File does not exist"
fi

echo $status