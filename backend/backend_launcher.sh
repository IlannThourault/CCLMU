#!/bin/activate

if [ -f "../.env" ];then
    source ../.env
else
    echo "Error : .env or ../.env not found"
    exit 1
fi

if [ -z "$PORT_BACKEND" ];then
    echo "Error : PORT_BACKEND not found"
    exit 1
else
    uvicorn backend:app --reload --port $PORT_BACKEND
fi