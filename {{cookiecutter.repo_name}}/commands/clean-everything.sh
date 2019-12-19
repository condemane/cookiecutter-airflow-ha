
#!/bin/bash
# clean and rebuild your docker images
echo "Now cleaning and rebuliding docker images "
docker kill $(docker ps -q)
docker-compose down -v
docker-compose rm -f
docker rmi -f $(docker images | grep "none" | awk '/ / { print $3 }')
# delete all images before the "until" date
# docker image prune -a --force --filter "until=2018-11-20T00:00:00"
# remove images created more than 10 days ago: 
# docker image prune -a --force --filter "until=240h"

# This cleans up your docker but do not remove your data :-)
screen ~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/tty
rm -r /var/lib/docker/overlay2/*

remove all the running containers (if using swarm, delete the stack)
docker stack rm <stack_name>

remove lingering containers
docker rm $(docker ps -a -q)

remove all image
docker rmi $(docker images -q)

stop docker service
service docker stop # or whatever: systctl ...

remove overlay2 files
sudo rm -rf /var/lib/docker/overlay2

start docker service
service docker start # or equally whatever: systcl...

re-deploy
docker stack deploy <deployment name>