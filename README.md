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

## Master-Slave Replication
````shell script
$ export GOOGLE_PROJECT=[name]
$ docker-machine create --driver google \
     --google-machine-image https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/family/ubuntu-1604-lts \
     --google-machine-type n1-standard-2 \
     monolith-db-slave
$ eval $(docker-machine env monolith-db-slave)
````

Open MySql port by adding firewall rule:
````shell script
$ gcloud compute firewall-rules create monolith-db-slave \
     --allow tcp:10101 \
     --target-tags=docker-machine \
     --description="Allow DB slave connections" \
     --direction=INGRESS 
````

Run containers:
````shell script
$ docker-compose -f docker-compose-replication.yml up -d
$ docker-compose -f docker-compose-replication.yml exec db_slave bash

````

Import actual DB Dump:
````shell script
$ mysql -h34.72.179.20 -uroot -p -P10101 app < dump/app_db.sql
````

Connect to MySql server and run the following command:
````sql
CHANGE MASTER TO
MASTER_HOST='34.78.37.195',
MASTER_PORT=10100,
MASTER_USER='root',
MASTER_PASSWORD='password',
MASTER_LOG_FILE='mysql-bin.000001',
MASTER_LOG_POS=0;

START SLAVE;
````

## Master-Slave Semisynchronous Replication
Install semi-sync plugin for master:
````shell script
docker-compose exec db mysql -uroot -p \
  -e "INSTALL PLUGIN rpl_semi_sync_master SONAME 'semisync_master.so';"
````

Install semi-sync plugins for slaves:
````shell script
docker-compose -f docker-compose-replication.yml exec db_slave mysql -uroot -p \
  -e "INSTALL PLUGIN rpl_semi_sync_slave SONAME 'semisync_slave.so';"

docker-compose -f docker-compose-replication.yml exec db_slave_1 mysql -uroot -p \
  -e "INSTALL PLUGIN rpl_semi_sync_slave SONAME 'semisync_slave.so';"
````

Enable semi-sync replication on master and show the result:
````shell script
docker-compose exec db mysql -uroot -p \
  -e "SET GLOBAL rpl_semi_sync_master_enabled = 1;" \
  -e "SHOW VARIABLES LIKE 'rpl_semi_sync%';"
````

Enable semi-sync replication on slaves and show the result:
````shell script
docker-compose -f docker-compose-replication.yml exec db_slave mysql -uroot -p \
  -e "SET GLOBAL rpl_semi_sync_slave_enabled = 1;" \
  -e "SHOW VARIABLES LIKE 'rpl_semi_sync%';"

docker-compose -f docker-compose-replication.yml exec db_slave_1 mysql -uroot -p \
  -e "SET GLOBAL rpl_semi_sync_slave_enabled = 1;" \
  -e "SHOW VARIABLES LIKE 'rpl_semi_sync%';"
````
