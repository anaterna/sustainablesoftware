#!/bin/bash

# Define the application directory
APP_DIR="../sb-app"

# Navigate to the application directory
cd "$APP_DIR" || { echo "Error: Failed to change directory to $APP_DIR"; exit 1; }

# Ensure Maven is installed (remove if already installed)
if ! command -v mvn &> /dev/null; then
    echo "Maven not found. Installing..."
    brew install maven
fi

# Clean and package the application
echo "Building the application..."
mvn clean package -DskipTests

# Build the Docker image
echo "Building Docker image..."
docker buildx build -f Dockerfile --platform linux/amd64 --tag spring-boot-app:latest --load .

# Run the Docker container
echo "Running the Docker container..."
docker run -d -p 8080:8080 -t spring-boot-app

# Give the application some time to start
sleep 10

echo "Application started successfully in Docker."
