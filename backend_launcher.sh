#!/bin/bash

if [ -f "backend/backend_launcher.sh" ]; then
    cd backend/
    bash backend_launcher.sh
else
    echo "Error backend/backend_launcher.sh not found"
    exit 1
fi