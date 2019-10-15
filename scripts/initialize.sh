#!/bin/sh
MAINDB="50043_DB"
PASSWDDB="password"

# creates a database and user named 50043_DB and gives the user all permissions for the 50043_DB database
mysql -e "CREATE DATABASE IF NOT EXISTS ${MAINDB} /*\!40100 DEFAULT CHARACTER SET utf8 */;"
mysql -e "CREATE USER IF NOT EXISTS ${MAINDB}@localhost IDENTIFIED BY '${PASSWDDB}';"
mysql -e "GRANT ALL PRIVILEGES ON ${MAINDB}.* TO '${MAINDB}'@'localhost';"
mysql -e "FLUSH PRIVILEGES;"

# import database # maybe dont need user to import database.. should be able to use root to import database.
echo "Enter password for MySQL"
mysql -u root -p < initialize.sql

