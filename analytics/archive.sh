#!/bin/bash

# Setup script for all nodes
HADOOP_VERSION="2.7.3"
HADOOP=hadoop-$HADOOP_VERSION
mkdir ~/server
cd ~/server

sudo apt-get -y install openjdk-8-jdk-headless
wget -nc https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/$HADOOP.tar.gz
tar -xf $HADOOP.tar.gz

cd $HADOOP/etc/hadoop
cp hadoop-env.sh temp
sed "s/\${JAVA_HOME}/\/usr\/lib\/jvm\/java-8-openjdk-amd64/" \
  temp > hadoop-env.sh