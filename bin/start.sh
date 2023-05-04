#!/usr/bin/env bash

if [ -d "venv" ]; then
    source venv/bin/activate
fi

export UVICORN_WORKERS="${UVICORN_WORKERS:=1}"
export PORT="${PORT:=8000}"

exec uvicorn cronitor_rum_relay.api:app --workers $UVICORN_WORKERS --proxy-headers --host 0.0.0.0 --port $PORT
