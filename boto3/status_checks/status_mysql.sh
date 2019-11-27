#!/bin/bash
# this script checks if the server has finished executing the user data script
# boot-finished file will be generated upon completion of user data script

public_ip="3.134.79.98"
keypair="50043-keypair"
username="ubuntu"

status=false
while [ $status == false ]
        do
                if ssh -o StrictHostKeyChecking=no -i ~/.ssh/$keypair.pem $username@$public_ip stat /var/lib/cloud/instance/boot-finished \> /dev/null 2\>\&1
                        then
                                status=true
                                echo "File exists, exiting loop"
                        else
                                status=false
                                echo "File does not exist"
                                sleep 5
                fi
        done
echo $status