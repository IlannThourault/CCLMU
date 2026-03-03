#!/bin/activate

if [ -f "../.public_env" ];then
    source ../.public_env
else
    echo "Error : .public_env or ../.public_env not found"
    exit 1
fi

if [ -z "$PORT_BACKEND" ];then
    echo "Error : PORT_BACKEND not found"
    exit 1
else
    uvicorn backend:app --reload --port $PORT_BACKEND
fi