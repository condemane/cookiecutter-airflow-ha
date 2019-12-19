echo "Building images"
docker-compose down
echo "Removing postgres_data"
sudo rm -rf postgres_data
echo "Removing old logs"
sudo rm -rf logs/*
echo "removing old csv files"
sudo rm -rf csv_exports/*
docker-compose build
echo "running images"
docker-compose up -d
echo "waiting 30 secs before continuing..."
sleep 10
echo "listing images"
docker ps
echo "Now scaling system to 15 workers"
if $1 == 'scale'
then
echo 'scaling the number of workers to: '$2
docker-compose scale worker=$2
fi
echo "updating scheduler"
docker-compose down airflow-scheduler
echo "listing images"
docker ps
echo "Yay, we're ready."
