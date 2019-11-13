#!/bin/bash

sudo mysql -e 'drop database if exists 50043_DB'
sudo mysql -e 'create database if not exists 50043_DB'
sudo mysql 50043_DB < 50043_DB.dump
