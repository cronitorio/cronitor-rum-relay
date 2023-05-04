#!/bin/bash

if [ -d "venv" ]; then
    source venv/bin/activate
fi

pip install -r requirements.txt

# Bind uvicorn process to container lifecycle
exec uvicorn cronitor_rum_relay.api:app --workers 1 --proxy-headers --host 0.0.0.0 --port 8000 --reload
