#!/bin/bash

open "http://localhost:5173?msg=please_reload_after_5s"
echo "Starting Movie Explorer Platform..."

# Ensure we are in the project root
cd "$(dirname "$0")"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker is not running. Please start Docker and try again."
  exit 1
fi

echo "Building and starting containers..."
docker-compose up --build
