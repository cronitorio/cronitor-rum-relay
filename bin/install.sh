#!/usr/bin/env bash

# check if virtual env exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

if [ -d "venv" ]; then
    source venv/bin/activate
fi

pip install -r requirements-dev.txt
