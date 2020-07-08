# Social Network

## Run
````shell script
$ cp .env.exapmple .env
$ docker-compose up -d
$ docker-compose exec monolith alembic upgrade head
````

## Deploy to GCP
````shell script
$ export GOOGLE_PROJECT=[name]
$ docker-machine create --driver google \
     --google-machine-image https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/family/ubuntu-1604-lts \
     --google-machine-type n1-standard-8 \
     --google-zone europe-west1-b \
     monolith
$ eval $(docker-machine env monolith)
$ docker-compose up -d
````

## Generate users
````shell script
$ flask user generate [count]
````

## WRK Report
Available at the following [link](https://github.com/antonLytkin18/otus-highload/blob/master/reports/wrk/wrk.ipynb)
