# Social Network

# Run
````shell script
$ cp .env.exapmple .env
$ docker-compose up -d
$ docker-compose exec monolith alembic upgrade head
````

# Deploy to GCP
````shell script
$ export GOOGLE_PROJECT=[name]
$ docker-machine create --driver google \
     --google-machine-image https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/family/ubuntu-1604-lts \
     --google-machine-type n1-standard-4 \
     --google-zone europe-west1-b \
     monolith
````

# Generate users
````shell script
$ flask user generate [count]
````
