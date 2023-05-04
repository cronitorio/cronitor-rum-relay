#!/usr/bin/env bash

if [ -d "venv" ]; then
    source venv/bin/activate
fi

pytest tests -vvv -s
