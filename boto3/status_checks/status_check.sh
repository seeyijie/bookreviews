#!/bin/bash
# this script checks if the server has finished executing the user data script
# boot-finished file will be generated upon completion of user data script
public_ip=$1
keypair=$2
username=$3

echo -e "\nChecking server status: (NOTE: ignore warnings for connection refused)"

status=false
while [ $status == false ]
        do
                if ssh -o StrictHostKeyChecking=no -i ~/.ssh/$keypair $username@$public_ip stat /var/lib/cloud/instance/boot-finished \> /dev/null 2\>\&1
                        then
                                status=true
                                echo -e "\nServer done with deployment. Transferring new IP addresses to server"
                                scp -i ~/.ssh/$keypair ./ip_addresses/*.txt $username@$public_ip:/home/$username
                        else
                                status=false
                                echo -n "."
                                sleep 3
                fi
        done
echo "Done"