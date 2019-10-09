#!/bin/sh
# current assumptions:
# database named 50043_DB does not exist before running script
# user '50043_DB'@'localhost' does not exist before running script

MAINDB="50043_DB"
PASSWDDB="password"

# creates a database and user named 50043_DB and gives the user all permissions for the 50043_DB database
mysql -e "CREATE DATABASE ${MAINDB} /*\!40100 DEFAULT CHARACTER SET utf8 */;"
mysql -e "CREATE USER ${MAINDB}@localhost IDENTIFIED BY '${PASSWDDB}';"
mysql -e "GRANT ALL PRIVILEGES ON ${MAINDB}.* TO '${MAINDB}'@'localhost';"
mysql -e "FLUSH PRIVILEGES;"

