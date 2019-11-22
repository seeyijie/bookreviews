# Automation scripts
The automation script launches 4 different instances and stores the IP addresses of the generated instances in `config_files` and `ip_addresses`.

## Prerequisite python3 libraries
* boto3
* fire
    * installed by `pip3 install fire`

To run the script, do `python3 launch_all.py --image=<image_id> --keyname=<key_pair>`. where `<image_id>` is an empty ubuntu 18.04 image and `<key_pair>` is the name of an existing .pem keypair which will be used to ssh into the servers.

Expected output:
```
Security Group Created sg-01fedfc8fd3c46b0d in vpc vpc-f4aa599f.
Ingress Successfully Set {'ResponseMetadata': {'RequestId': '1af7fbe3-8cdd-4f93-b797-41aced6c686d', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8', 'content-length': '259', 'date': 'Fri, 22 Nov 2019 03:14:29 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}

******** react server info ********
new instance: i-01a7eea0ed7e85de6
3.134.81.0
50043-keypair
2019-11-22 03:14:31+00:00

******** mongodb server info ********
new instance: i-0624c472f8c840d78
3.134.80.144
50043-keypair
2019-11-22 03:14:31+00:00

******** mysql server info ********
new instance: i-04e7d7ba560798fcd
3.18.108.95
50043-keypair
2019-11-22 03:14:31+00:00

******** flask server info ********
new instance: i-043413db0b25b6633
18.216.140.194
50043-keypair
2019-11-22 03:14:31+00:00
```