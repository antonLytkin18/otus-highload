#!/bin/bash

echo "Apply database migrations"
alembic upgrade head

echo "Starting server"
python app.py
