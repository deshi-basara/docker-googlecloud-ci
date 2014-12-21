# Version 0.0.1
# Docker bersion 1.4.1
#
# Usage:    sudo docker build -t "<username>/docker-googlecloud-ci-nodejs" .
#           sudo docker run -i -d <username>/docker-googlecloud-ci-nodejs /bin/bash

# Fetch the latest ubuntu lts
FROM    ubuntu:14.04



# setup global dependencies programms
RUN     sudo apt-get install -y curl git screen software-properties-common
# setup the redis-database server repository
RUN     sudo add-apt-repository -y ppa:chris-lea/redis-server


# setup curl and the nodejs repository
RUN     curl -sL https://deb.nodesource.com/setup | sudo bash -
# install nodejs, its dependency the node package manager and the redis-server
RUN     sudo apt-get update && sudo apt-get install -y nodejs redis-server
# install the sailsjs version 0.10.5
RUN     sudo npm install -g sails@0.10.5



# bunde app sources
COPY    . /src



# expose sailsjs port
EXPOSE  1337