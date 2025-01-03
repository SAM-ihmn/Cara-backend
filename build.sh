#!/bin/bash

# Usage function to display help
usage() {
    echo "Usage: $0 [build|production]"
    exit 1
}

# Check if the argument is provided
if [ -z "$1" ]; then
    usage
fi

MODE=$1

# Validate the mode
if [[ "$MODE" != "build" && "$MODE" != "production" ]]; then
    echo "Error: Invalid mode. Use 'build' or 'production'."
    usage
fi

# Run the Docker build command with the appropriate mode
echo "Building Docker image in $MODE mode..."
docker build --build-arg MODE=$MODE -t my-app .

if [ $? -eq 0 ]; then
    echo "Docker image built successfully in $MODE mode."
else
    echo "Failed to build Docker image."
    exit 1
fi
