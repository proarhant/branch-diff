#!/bin/bash

cd ./branch-diff

echo "Removing image..."
echo "..."

app="git-flask"
docker-compose stop
docker-compose down

#Just making sure...
echo "Deleting ${app} image..."
docker rmi $(docker images | grep -i ${app})
echo "Cleanup script completed."
