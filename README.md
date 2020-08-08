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
<details>
<summary>Click to expand</summary>
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
</details>

## Master-Slave Semisynchronous Replication
<details>
<summary>Click to expand</summary>
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
</details>

## Sharding via Vitess
<details>
<summary>Click to expand</summary>

### Preparing environment

Create GCP instance:
````shell script
docker-machine create --driver google \
     --google-machine-image https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/family/ubuntu-1604-lts \
     --google-machine-type n1-standard-4 \
     vitess
eval $(docker-machine env vitess)
````

Open MySql port by adding firewall rule:
````shell script
gcloud compute firewall-rules create vitess \
     --allow tcp:15000,tcp:15001,tcp:15306 \
     --target-tags=docker-machine \
     --description="Sharing vitess ports" \
     --direction=INGRESS
````

Clone vitess repository and run it using docker:
```shell script
git clone https://github.com/vitessio/vitess.git
cd vitess/ && docker build -f docker/local/Dockerfile -t vitess/local .
docker run -p 15000:15000 -p 15001:15001 -p 15306:15306 --rm -it vitess/local
```

Run application with master database:
````
docker-compose up -d
````

Run replica databases:
````
docker-compose -f docker-compose-replication.yml up -d
````

### Move source tables to reshard

Create Vttablet using current master and replica databases:
```shell script
vttablet \
 $TOPOLOGY_FLAGS \
 -logtostderr \
 -tablet-path "zone1-0000000200" \
 -init_keyspace app \
 -init_shard 0 \
 -init_tablet_type replica \
 -port 15200 \
 -grpc_port 16200 \
 -service_map 'grpc-queryservice,grpc-tabletmanager,grpc-updatestream' \
 -db_host 35.195.211.151 \
 -db_port 10100 \
 -db_repl_user root \
 -db_repl_password password \
 -db_filtered_user root \
 -db_filtered_password password \
 -db_app_user root \
 -db_app_password password \
 -db_dba_user root \
 -db_dba_password password \
 -init_db_name_override app \
 -init_populate_metadata \
 > $VTDATAROOT/$tablet_dir/vttablet.out 2>&1 &

vttablet \
 $TOPOLOGY_FLAGS \
 -logtostderr \
 -tablet-path "zone1-0000000201" \
 -init_keyspace app \
 -init_shard 0 \
 -init_tablet_type replica \
 -port 15201 \
 -grpc_port 16201 \
 -service_map 'grpc-queryservice,grpc-tabletmanager,grpc-updatestream' \
 -db_host 35.195.211.151 \
 -db_port 10101 \
 -db_repl_user root \
 -db_repl_password password \
 -db_filtered_user root \
 -db_filtered_password password \
 -db_app_user root \
 -db_app_password password \
 -db_dba_user root \
 -db_dba_password password \
 -init_db_name_override app \
 -init_populate_metadata \
 > $VTDATAROOT/$tablet_dir/vttablet.out 2>&1 &
```

Mark first Vttablet as master:
````shell script
vtctlclient InitShardMaster -force app/0 zone1-200
````

Create new Keyspace for resharding:
````shell script
vtctl $TOPOLOGY_FLAGS CreateKeyspace -sharding_column_name=chat_id chat_message
````

Create new Vttablets for single shard:
````shell script
for i in 300 301; do
 CELL=zone1 TABLET_UID=$i ./scripts/mysqlctl-up.sh
 CELL=zone1 KEYSPACE=chat_message TABLET_UID=$i ./scripts/vttablet-up.sh
done
````

Mark first Vttablet as master:
````shell script
vtctlclient InitShardMaster -force chat_message/0 zone1-300
````

Move table `chat_message`:
````shell script
vtctlclient MoveTables -workflow=app2chat_message app chat_message '{"chat_message":{}}'
````

Show the difference between two sources:
````shell script
vtctlclient VDiff chat_message.app2chat_message

````

Switch read and write operations without downtime:
````shell script
vtctlclient SwitchReads -tablet_type=rdonly chat_message.app2chat_message
vtctlclient SwitchReads -tablet_type=replica chat_message.app2chat_message

vtctlclient SwitchWrites chat_message.app2chat_message
````

Switch application database connection credentials using for `chat_message` table.  
VTGate credentials:
````.env
CHAT_MYSQL_HOST=34.66.217.5
CHAT_MYSQL_PORT=15306
CHAT_MYSQL_USER=mysql_user
CHAT_MYSQL_PASSWORD=mysql_password
CHAT_MYSQL_ROOT_PASSWORD=mysql_password
CHAT_MYSQL_DB=chat_message
````

Drop source table:
````shell script
vtctlclient DropSources chat_message.app2chat_message
````

Now application use VTGate connection to serve all operations with table `chat_message`.

### Resharding from `0` to `-80, 80-` shards without downtime

Create new Vttablets for shards `-80, 80-`:
````shell script
for i in 400 401; do
 CELL=zone1 TABLET_UID=$i ./scripts/mysqlctl-up.sh
 SHARD=-80 CELL=zone1 KEYSPACE=chat_message TABLET_UID=$i ./scripts/vttablet-up.sh
done

vtctlclient InitShardMaster -force chat_message/-80 zone1-400

for i in 500 501; do
 CELL=zone1 TABLET_UID=$i ./scripts/mysqlctl-up.sh
 SHARD=80- CELL=zone1 KEYSPACE=chat_message TABLET_UID=$i ./scripts/vttablet-up.sh
done

vtctlclient InitShardMaster -force chat_message/80- zone1-500
````

Create and apply VSchema for table `chat_message`. Sharding function is `reverse_bits`.
````shell script
echo '{
    "sharded": true,
    "vindexes": {
      "hash_f": {
        "type": "reverse_bits"
      }
    },
    "tables": {
      "chat_message": {
        "column_vindexes": [
          {
            "column": "chat_id",
            "name": "hash_f"
          }
        ]
      },
      "/.*": {
        "column_vindexes": [
          {
            "column": "chat_id",
            "name": "hash_f"
          }
        ]
      }
    }
}' > chat_vschema.json

vtctl $TOPOLOGY_FLAGS ApplyVSchema -vschema_file=chat_vschema.json chat_message
rm -f chat_vschema.json
````

Reload schema keyspace:
````shell script
vtctlclient ReloadSchemaKeyspace -concurrency=10 chat_message
````

Run resharding:
````shell script
vtctlclient Reshard chat_message.chat2chat '0' '-80,80-'
````

Show the difference between two sources:
````shell script
vtctlclient VDiff chat_message.chat2chat
````

Switch read and write operations without downtime:
````
vtctlclient SwitchReads -tablet_type=rdonly chat_message.chat2chat
vtctlclient SwitchReads -tablet_type=replica chat_message.chat2chat

vtctlclient SwitchWrites chat_message.chat2chat
````

Delete source shard:
````shell script
vtctlclient DeleteShard -recursive chat_message/0
````

### Resharding from `-80` to `-40, 40-80` shards without downtime

Create new Vttablets for shards `-40, 40-80`:

````shell script
for i in 600 601; do
 CELL=zone1 TABLET_UID=$i ./scripts/mysqlctl-up.sh
 SHARD=-40 CELL=zone1 KEYSPACE=chat_message TABLET_UID=$i ./scripts/vttablet-up.sh
done

vtctlclient InitShardMaster -force chat_message/-40 zone1-600

for i in 700 701; do
 CELL=zone1 TABLET_UID=$i ./scripts/mysqlctl-up.sh
 SHARD=40-80 CELL=zone1 KEYSPACE=chat_message TABLET_UID=$i ./scripts/vttablet-up.sh
done

vtctlclient InitShardMaster -force chat_message/40-80 zone1-700
````

Run resharding:
````shell script
vtctlclient Reshard chat_message.chat2chat-80 '-80' '-40,40-80'
````

Show the difference between two sources:
````shell script
vtctlclient VDiff chat_message.chat2chat-80
````

Switch read and write operations without downtime:
````shell script
vtctlclient SwitchReads -tablet_type=rdonly chat_message.chat2chat-80
vtctlclient SwitchReads -tablet_type=replica chat_message.chat2chat-80

vtctlclient SwitchWrites chat_message.chat2chat-80
````

Delete source shard:
````shell script
vtctlclient DeleteShard -recursive chat_message/-80
````
</details>
