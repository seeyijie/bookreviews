# 50.043 Database Project

## Prerequisite python3 libraries
* boto3
* fire
    * installed by `pip3 install fire`
* dos2unix (for WSL users only)
    * `sudo apt-get install dos2unix`

## Other dependencies
* openssh-server
* openssh-client

## Other requirements
* Please make sure that no security group named `50043_SECURITY_GROUP` exists in your aws user account.

## Instructions to launch automation script
* **Caveats (There's no free lunch)**: 
    * The data extraction was tested to use **t3.large** and above. Lower tier instances hang on our data extraction step from the database.
    * the automation script takes in the **path to your IAM credentials csv file** in the `--csv_aws_credentials`, and the image_id for **us-east-1** in the `--image_id` argument.
* from the `boto3` folder, run `python3 call_master.py --csv_aws_credentials=<path/to/csv/> --image_id=<ami_image_id> --instance_type=<instance_type>`.
* Example: `python3 call_master.py --csv_aws_credentials=/home/ubuntu/Downloads/.aws/credentials.csv --image_id=ami-04b9e92b5572fa0d1 --instance_type=t3.large`
* We have included a termination script to terminate the instances launched by `call_master.py`. To run the script, go to `boto3` and run `python3 terminate_backend.py`.

## Automation script
The automation script is located in `bookreviews/boto3/call_master.py`. It launches 4 EC2 instances and installs mysql, mongodb, flask and react on them. Text files and shell script files will be generated on your local machine. After the 4 servers are deployed, the server copies the IP addresses of all the new servers and transfers them into all the other servers. After deployment, follow the link generated in the command line. This will take you to our home page. Enjoy!

**NOTES TO USER:**
* Please make sure your AWS user account is in `us-east-1`
* Please make sure you have a good internet connection when you try and run the automation scripts.
* This script requires you to use python 3.7 and above because we use `fstrings`. If `python3` does not use python 3.7 and above by default, install python3.7 and use `python3.7` to run the scripts instead (or make an alias for python3).
* if you see the warning `ssh connection refused`, let the script continue to run. It should eventually add the IP address of the particular server into your `~/.ssh/known_hosts` file.
* This script is meant to run on **UNIX based systems (linux or MacOS)**. If you use windows subsystem for linux (WSL), please run `dos2unix` on `bookreviews/boto3/status_checks/status_check.sh` and `bookreviews/boto3/master.sh`. This is because windows has different file line endings than unix.

**Expected output:**
First, you should see that the script creates a security group.

```
Security Group Created sg-01fedfc8fd3c46b0d in vpc vpc-f4aa599f.
Ingress Successfully Set {'ResponseMetadata': {'RequestId': '1af7fbe3-8cdd-4f93-b797-41aced6c686d', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8', 'content-length': '259', 'date': 'Fri, 22 Nov 2019 03:14:29 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}
```
Then, you should observe that the servers are being launched via boto3. You would see the details of the servers being printed to the console. Launching the servers generate several text files and bash scripts inside `boto3/ip_addresses` and `boto3/config_files` respectively.
```
******** mongodb server info ********
new instance: i-0e89b57f6c8c2e77f
18.222.205.153
50043-keypair
2019-12-03 14:21:49+00:00

******** mysql server info ********
new instance: i-0d97337cf8702863f
13.58.169.137
50043-keypair
2019-12-03 14:22:22+00:00

******** flask server info ********
new instance: i-03c8be10d66d5bac3
3.14.147.43
50043-keypair
2019-12-03 14:22:54+00:00

******** react server info ********
new instance: i-04c733c0b36cdaad4
18.189.31.214
50043-keypair
2019-12-03 14:23:27+00:00
```
After which, the script starts checking if the servers have finished running the user data scripts. This will take awhile. so grab a cup of coffee and prepare to be amazed.
```
Server deployment done. Checking status of mysql.

Checking server status: (NOTE: ignore warnings for connection refused)
Warning: Permanently added '13.58.169.137' (ECDSA) to the list of known hosts.
.................................................
```
Once the servers have been deployed successfully, the script transfers the newly generated IP addresses and `config.js` file into every server.
```
Server done with deployment. Transferring new IP addresses to server
config_flask_ip.txt                                                                                                                                                                              100%   11     0.0KB/s   00:00    
config_mongodb_ip.txt                                                                                                                                                                            100%   14     0.1KB/s   00:00    
config_mysql_ip.txt                                                                                                                                                                              100%   13     0.1KB/s   00:00    
config_react_ip.txt                                                                                                                                                                              100%   13     0.1KB/s   00:00    
Done
```
Then the script runs the new flask and react servers. This installs sets up and installs a couple of software packages into the react server before being fully operational. Lastly, a link will be printed to the console for you to access our project via any browser.
```
*************************************************
Deployment done! Thank you for your patience! 
Access the webpage via the following link: http://18.189.31.214:80
```
