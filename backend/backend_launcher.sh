#!/bin/activate

# Création du venv si besoin
if [ ! -d "backend_venv" ];then
    python3 -m venv backend_venv
fi

# Activation du venv
CURRENT_SHELL=$(basename "$SHELL")
if [[ CURRENT_SHELL == "fish" ]];then
    source backend_venv/bin/activate.fish
else
    source backend_venv/bin/activate
fi

# Freeze requirements
if [[ $1 == "freeze" ]];then
    pip freeze > .requirements
fi

# Installation des requirements
if [ -f ".requirements" ];then
    pip install -r .requirements
else
    echo "Error : .requirements file needed"
    exit 1
fi

# Démarrage du serveur
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