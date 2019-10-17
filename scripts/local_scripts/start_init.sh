#!/bin/bash

echo "Installing dos2unix"
sudo apt-get --assume-yes install dos2unix

echo "\nConverting initialize.sh to be compatible with Windows Subsystem for Linux"
dos2unix initialize.sh

echo "\nExecuting initialization scripts"
sudo ./initialize.sh