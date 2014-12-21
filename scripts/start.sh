#! /bin/bash
#
# Usage: ./start.sh [<GIT_REPO_URL>] [<APP_START_CMD] [<GIT_COMMIT>]
#
# Example: ./start.sh https://github.com/deshi-basara/angular-gulp-seed.git "bower install" d7b731d2fe8bde4c509c5f6ed29e7873c530b7f2
#
# or       ./start.sh https://github.com/deshi-basara/angular-gulp-seed.git "bower install"
#
#


####### Constants
#GIT_REPO_NAME="angular-gulp-seed"
GIT_REPO_URL="$1"
GIT_COMMIT="$3"

APP_START_CMD="$2"






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
# 2) Pull Repo
#
##
echo "========================================================================================"
echo "2) Pulling Git-Repo"
echo "========================================================================================"

# clone the repo and check if the clone was successfully
(git clone "$GIT_REPO_URL" && cd *) || {
    echo
    echo 'START-ERROR: git clone failed'
    echo
    exit 1
}

# does the user wish to start a specific commit?
if [ ! -z "$GIT_COMMIT" ]; then
    # reset the repo back to the commit
    echo
    (cd * && git reset --hard "$GIT_COMMIT") || {
        echo
        echo 'START-ERROR: git reset failed'
        echo
        exit 1
    }
    echo
fi

echo
echo

# check if the repo was pulled succesfully
#if [ "$(ls */)" ] ; then
#    echo "$GIT_REPO_URL was pulled"
#else
#    echo "$GIT_REPO_URL does not exist"
#    exit 1
#fi



##
#
# 3) Upstart the application with the handed command
#
##
echo "========================================================================================"
echo "3) Upstarting the application"
echo "========================================================================================"

(cd * && ${APP_START_CMD}) || {
    echo
    echo 'START-ERROR: git clone failed'
    echo
    exit 1
}

echo
echo