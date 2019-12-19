echo "Building images"
docker-compose down
echo "Removing postgres_data"
rm -rf postgres_data
echo "Removing old logs"
rm -rf logs/*
echo "removing old csv files"
rm -rf csv_exports/*
docker-compose build
echo "running images"
docker-compose up
echo "**************************************************************************************************************"
echo "To access dashboard, please visit: http://localhost:8080/admin/"
echo "To access scheduler monitor, please visit: http://localhost::5555/dashboard"
echo "**************************************************************************************************************"
