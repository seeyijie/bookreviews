# How to run scripts
1. Firstly, change the IP addresses and keys in the config files to the IP and key for the EC2 instance. These files are found in the `config` folder under this directory.
2. Run scripts without sudo permissions

# Commands used for debugging scripts

## Adding fingerprints of servers to local machine's known hosts
* To check if an server is in the list of known hosts. Returns nothing if theres no key inside
    * `ssh-keygen -F 3.16.187.168`
* To remove fingerprint
    * `ssh-keygen -R 3.16.187.168`
This is an indication that the hosts have been removed from the known_hosts file successfully
```
$ ssh-keygen -R 18.219.178.148
# Host 18.219.178.148 found: line 42
# Host 18.219.178.148 found: line 43
# Host 18.219.178.148 found: line 44
/home/dominic/.ssh/known_hosts updated.
Original contents retained as /home/dominic/.ssh/known_hosts.old
```
* To add fingerprint
    * `ssh-keyscan -t ecdsa -H 3.16.187.168 >> ~/.ssh/known_hosts`
    * **NOTE** must use -t ecdsa to specify the type of key to fetch from the scanned host. Defaults to fetch 3 keys. Probably had errors because the system was trying to validate differently encrypted keys.

This is an indication that the default 3 keys (rsa, ecdsa, ed25519) have been added into ~/.ssh/known_hosts
```
$ ssh-keyscan -H 18.219.178.148 >> ~/.ssh/known_hosts
# 18.219.178.148:22 SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3
# 18.219.178.148:22 SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3
# 18.219.178.148:22 SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3
```