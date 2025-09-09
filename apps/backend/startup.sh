#!/bin/bash
# run migration and start server
# load environment variables
export $(grep -v '^#' .env | xargs -d '\n')

# install Python requirements
pip install -r requirements.txt

# run migrations
alembic upgrade head

# start server
uvicorn app.main:app --reload
