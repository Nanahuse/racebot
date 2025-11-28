#!/bin/bash
set -e

# Copy host ssh config if present
if [ -d /tmp/host-ssh ]; then
    mkdir -p ~/.ssh
    cp -r /tmp/host-ssh/* ~/.ssh/
    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/* || true
fi
