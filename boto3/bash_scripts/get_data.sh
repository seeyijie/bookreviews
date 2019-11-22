#!/bin/bash

# Extension of prof's script
# Creates a folder data_store under project root directory to store the datasets

# Create data folder in parent directory
cd ~/bookreviews
mkdir data_store
cd data_store

# Get Kindle reviews
wget -c https://www.dropbox.com/s/wg4y0etqwml0dgg/kindle-reviews.zip?dl=0 -O kindle-reviews.zip
unzip kindle-reviews.zip
rm -rf kindle_reviews.json

# Get meta data
wget -c https://www.dropbox.com/s/zmysok83e8a4vqh/meta_kindle_store.zip?dl=0 -O meta_kindle_store.zip
unzip meta_kindle_store.zip

# Clean up
rm -rf *.zip
