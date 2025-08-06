#!/usr/bin/env bash
# Optimized build script for Render deployment
# Installs FFmpeg and other system dependencies efficiently

echo "Installing system dependencies..."

# Update package list and install FFmpeg in one command to reduce layers
apt-get update && apt-get install -y ffmpeg python3-dev build-essential && \
apt-get clean && \
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

echo "System dependencies installed successfully!" 