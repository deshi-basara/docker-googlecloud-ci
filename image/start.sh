#! /bin/bash
#
# Custom commands that start the application after fetching the repository.
#

# client & server config
cd client && npm install && bower install && cd ..
cd server && npm install

# run redis
service redis-server start

# run server
#screen -d -m cd server && sails lift
cd server && sails lift