#!/usr/bin/env bash

if [ -d "venv" ]; then
    source venv/bin/activate
fi

black cronitor_rum_relay
