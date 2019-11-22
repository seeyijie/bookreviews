# How to run scripts
1. Firstly, change the IP addresses and keys in the config files to the IP and key for the EC2 instance. These files are found in the `config` folder under this directory.
2. Run scripts **without** sudo permissions (affects where fingerprints of servers are placed)

# Scripts description
## Folder structure
### `config`
contains configuration files for each of the three EC2 servers. These scripts contain the IP addresses of the servers as well as which key is to be used to ssh into them. These configuration files will be referenced by the other scripts and serves as a **central location** for updating the IP addresses of the servers.

### `backup_scripts` folder
contains scripts are used to backup the EC2 servers. Backup files will live on the server. Restoration is also done from the backup files in the server itself.
* `backup_mysql.sh`
    * change the `server_ip` and `public_key` variables in `config/config_mysql.sh` to that of the server
    * to run, execute `./backup_mysql.sh`
    * This creates a dump file in the mysql server. by the name `50043_DB.dump` in the directory `/home/ubuntu`.

* `restore_mysql.sh`
    * change the `server_ip` and `public_key` variables in `config/config_mysql.sh` to that of the server
    * to run, execute `./restore_mysql.sh`

### `master_scripts` folder
this folder contains the scripts that can be run from our local machine. To run, simply make sure the config files are up to date with the correct IP addresses and keys. Then, run the scripts.
* `clear_<server>.sh`
    * deletes all non hidden files in the home directory of the servers
    * to run, `./clear_<server>.sh`, where `<server>` should be replaced with `flask`, `mongodb` or `mysql`

* `deploy_all.sh`
    * deploys all servers in 3 different EC2 instances. Adds server fingerprint to `~/.ssh/known_hosts` in your local machine before execution and deletes it after execution. This is to bypass key checking prompts by ssh in a secure manner.
    * NOTE: comment and uncomment the parts of the script as needed

* `reset_all.sh`
    * does the same thing as `clear_<server>.sh`, except it does it on all servers

### `flask` folder
contains scripts that will be called by the master scripts

### `mongodb` folder
contains scripts that will be called by the master scripts

### `mysql` folder
contains scripts that will be called by the master scripts

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