#!/bin/bash

if [ -f "backend/backend_launcher.sh" ]; then
    cd backend/
    if [[ -z $1 ]];then
        bash backend_launcher.sh
    else
        bash backend_launcher.sh $1
    fi
else
    echo "Error backend/backend_launcher.sh not found"
    exit 1
fi