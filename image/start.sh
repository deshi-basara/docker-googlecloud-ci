#! /bin/bash
#
# Custom commands that start the application after fetching the repository.
#

# install missing server dependencies
(cd /src/server; npm install)

# run redis database server
service redis-server start

# run server
(cd /src/server; forever start app.js --prod)