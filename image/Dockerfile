# Version 0.0.1
# Docker bersion 1.4.1
#
# Usage:    sudo docker build -t "<username>/docker-googlecloud-ci-nodejs" .
#           sudo docker run -i -d <username>/docker-googlecloud-ci-nodejs /bin/bash

# Fetch the latest ubuntu lts
FROM    ubuntu:14.04

# setup missing programms
RUN     sudo apt-get install -y curl git
# setup curl and the nodejs repository
RUN     curl -sL https://deb.nodesource.com/setup | sudo bash -
# install nodejs & its dependency the node package manager
RUN     sudo apt-get update && sudo apt-get install -y nodejs
# install the latest express version 4.10.6
RUN     sudo npm install -g express@4.10.6



# bunde app sources
COPY    . /src



# expose express port
EXPOSE  3000