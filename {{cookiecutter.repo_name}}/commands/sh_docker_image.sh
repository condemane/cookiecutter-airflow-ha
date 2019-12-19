#!/bin/bash
# move into the docker image terminal

echo -e "Enter the container ID(first few characters): "
read c_id
echo "Now moving this terminal to the container $c_id"
docker exec -it $c_id /bin/bash