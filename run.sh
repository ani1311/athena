#!/bin/bash

# This script runs the Python application, loading environment variables from a .secrets file if it exists.

# Check for the .secrets file
if [ -f .secrets ]; then
  echo "Loading environment variables from .secrets"
  # `set -a` exports all variables created or modified
  set -a
  source .secrets
  # `set +a` stops exporting
  set +a
else
  echo "Info: .secrets file not found, skipping."
fi

# Run the main application using uv, passing along any script arguments
uv run main.py "$@"
