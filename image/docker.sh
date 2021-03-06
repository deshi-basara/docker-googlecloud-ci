#! /bin/bash
#
# Fetches a handed git-repository and executes the specified "APP_START_CMD"-script.
#
# Usage:   ./docker.sh


####### Constants

# get value from the google-meta-data and not from cli
GIT_REPO_URL=$(curl http://metadata/computeMetadata/v1/instance/attributes/url -H "Metadata-Flavor: Google")
GIT_COMMIT=$(curl http://metadata/computeMetadata/v1/instance/attributes/commit -H "Metadata-Flavor: Google")
APP_START_CMD=$(curl http://metadata/computeMetadata/v1/instance/attributes/start -H "Metadata-Flavor: Google")

echo $GIT_COMMIT

####### Main

##
#
# 1) Validate input
#
##
echo "========================================================================================"
echo "4/6 Validating Input"
echo "========================================================================================"

# Does the repo exist?
if [ -z "$GIT_REPO_URL" ]; then
    echo "GIT_REPO_URL was not set"
    exit 1
else
    echo "GIT_REPO_URL=$GIT_REPO_URL"
fi

# Does the command exist?
if [ -z "$APP_START_CMD" ]; then
    echo "APP_START_CMD was not set"
    exit 1
else
    echo "APP_START_CMD=$APP_START_CMD"
fi

echo
echo



##
#
# 2) Pull Repo into the current folder
#
##
echo "========================================================================================"
echo "5/6 Pulling Git-Repo"
echo "========================================================================================"

# clone the repo inside the current directory (git clone creates a new directory, that's why we have to
# use a little workaround)
(
git init &&
git remote add origin "$GIT_REPO_URL" &&
git fetch &&
git branch master origin/master &&
git checkout master
) || {
    echo
    echo 'START-ERROR: git clone failed'
    echo
    exit 1
}

# does the user wish to start a specific commit?
if [ ! -z "$GIT_COMMIT" ]; then
    # reset the repo back to the commit
    echo
    git reset --hard "$GIT_COMMIT" || {
        echo
        echo 'START-ERROR: git reset failed'
        echo
        exit 1
    }
    echo
fi

echo
echo



##
#
# 3) Upstart the application with the handed command
#
##
echo "========================================================================================"
echo "6/6 Upstarting the application"
echo "========================================================================================"

(chmod +x "/src/$APP_START_CMD" && /bin/bash "/src/$APP_START_CMD") || {
    echo
    echo 'START-ERROR: upstart failed'
    echo
    exit 1
}

echo
echo



##
#
# 4) Give success message
#
##
echo "========================================================================================"
echo "Success ... Application was deployed to IP: $(curl "http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip" -H "Metadata-Flavor: Google")"
echo "========================================================================================"