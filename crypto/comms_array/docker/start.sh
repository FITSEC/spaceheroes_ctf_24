#!/bin/bash

if [ -z "$PORT" ]; then
    export PORT=1234
fi

socat \
    tcp4-listen:${PORT},fork,reuseaddr \
    system:"timeout 1 python3 comms_array.py"
