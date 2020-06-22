# Social Network

# Run
````shell script
cp .env.exapmple .env
docker-compose up -d
docker-compose exec monolith alembic upgrade head
````

# Generate users
````shell script
flask user generate [count]
````
