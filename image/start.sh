#! /bin/bash
#
# Custom commands that start the application after fetching the repository.
#

# install missing server dependencies
(cd /src/server; npm install)

# run redis database server
service redis-server start

# run server
(forever start /src/server/app.js --prod)