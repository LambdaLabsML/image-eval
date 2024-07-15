#!/bin/bash

# Function to handle errors
handle_error() {
    echo "Error occurred in script at line: $1"
    exit 1
}

# Trap errors
trap 'handle_error $LINENO' ERR

# Default hostname
DEFAULT_HOSTNAME="imageeval"

# Read hostname parameter or use default
HOSTNAME="${1:-$DEFAULT_HOSTNAME}"

# Navigate to models/opensora directory
cd models/opensora || { echo "Failed to navigate to models/opensora directory"; exit 1; }

# Copy the deploy script to the remote host and execute it
scp remote_deploy.sh ubuntu@${HOSTNAME}:/tmp/ && \
ssh ubuntu@${HOSTNAME} 'chmod +x /tmp/remote_deploy.sh && /tmp/remote_deploy.sh' || { echo "Failed to deploy and execute script on remote host"; exit 1; }

echo "Script executed successfully on ${HOSTNAME}"
