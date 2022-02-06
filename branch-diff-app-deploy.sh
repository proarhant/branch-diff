#!/bin/bash

usage() { echo "Usage: $0 [-m local|detached]" 1>&2; exit 1; }

while getopts ":h:m:" flag; do
    case "${flag}" in
        m)
            DEBUG_MODE=${OPTARG}
            ;;
        *)
            usage
            exit 0
            ;;
    esac
done

#Clone the git repo under "branch-diff" dir
echo ""
[ -d "./branch-diff/repo" ] && echo "The existence of repo dir implies Git repo is ready." || git clone https://github.com/proarhant/branch-diff.git branch-diff/repo

sleep 3

app="git-flask"
echo ""

cd branch-diff
#Just making sure...
docker-compose down
echo ""

if [ "${DEBUG_MODE}" == 'local' ]; then
    echo "Starting the app instance in local mode without Docker..."
    python3 main.py 
elif [ "${DEBUG_MODE}" == 'detached' ]; then
    echo "Starting the app instance in detached mode..."
    docker-compose build --no-cache
    sleep 3
    docker-compose up -d
else
    echo "The ${app} container running in console mode...";
    docker-compose build --no-cache
    sleep 3
    docker-compose up
    echo ""
    echo "=== Notes:"
    echo "    Examples: http://0.0.0.0/git/scan?an=pro   http://0.0.0.0/git/scan?sb=featureBranch&since=18&an=Pro"
    echo "    Date on the browser is in UTC."
    echo "    Please see README.md for details."
    echo "==="
fi
