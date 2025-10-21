#!/bin/bash

# ARC CMS Backend Deployment Wrapper
# This script calls the actual deployment script from the deployment folder

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the deployment directory and run the deployment script
cd "$SCRIPT_DIR/deployment"
./deploy.sh "$@"
