#!/bin/bash

# Extension of prof's script
# Creates a folder data_store under project root directory to store the datasets

# Create data folder in parent directory
cd /home/ubuntu/bookreviews # cannot use ~ in user data. will go to root folder
mkdir data_store
cd data_store

# Get Kindle reviews
wget -c https://istd50043.s3-ap-southeast-1.amazonaws.com/kindle-reviews.zip -O kindle-reviews.zip
unzip kindle-reviews.zip
rm -rf kindle_reviews.json

# Get meta data
wget -c https://istd50043.s3-ap-southeast-1.amazonaws.com/meta_kindle_store.zip -O meta_kindle_store.zip
unzip meta_kindle_store.zip

# Clean up
rm -rf *.zip
