#!/bin/bash

# Variables
name_dir="ass1-dir"
name_file="text.txt"
default_project="protean-theater-429506-s7"

# Create directory
mkdir -p $name_dir
echo "Successfull creating directory $name_dir"

# Create text file
cd $name_dir
touch $name_file
echo "Hello Yessimseit Manarbek" >> $name_file
echo "Successfully create $name_file"

# Set default gcloud project
gcloud config set project $default_project
echo "Successfully set default Google Cloud project $default_project"

# check all work
ls ./$name_dir
cat ./$name_dir/$name_file
gcloud config get-value project
