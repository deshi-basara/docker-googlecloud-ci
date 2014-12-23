#! /bin/bash
#
# Fetches a handed git-repository and starts the containing "start.sh".
#
#
# Usage:   ./docker.sh [<GIT_REPO_URL>] [<GIT_COMMIT>]
#
# Example: ./docker.sh https://github.com/deshi-basara/glftv-video-processor-web.git d7b731d2fe8bde4c509c5f6ed29e7873c530b7f2
#
# or       ./docker.sh https://github.com/deshi-basara/glftv-video-processor-web.git "bower install"
#


####### Constants
#GIT_REPO_NAME="angular-gulp-seed"
#GIT_REPO_URL="$1"
#GIT_COMMIT="$3"
#APP_START_CMD="start.sh"

# get value from the google-meta-data and not from cli
GIT_REPO_URL=$(curl http://metadata/computeMetadata/v1/instance/attributes/url -H "Metadata-Flavor: Google")
GIT_COMMIT=$(curl http://metadata/computeMetadata/v1/instance/attributes/commit -H "Metadata-Flavor: Google")
APP_START_CMD=$(curl http://metadata/computeMetadata/v1/instance/attributes/start -H "Metadata-Flavor: Google")

####### Main

##
#
# 1) Validate input
#
##
echo "========================================================================================"
echo "1) Validating Input"
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
echo "2) Pulling Git-Repo"
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
echo "3) Upstarting the application"
echo "========================================================================================"

(chmod +x "$APP_START_CMD" && sh "$APP_START_CMD") || {
    echo
    echo 'START-ERROR: upstart failed'
    echo
    exit 1
}

echo
echo
