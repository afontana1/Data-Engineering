#!/bin/bash
set -e

# ---------------------------------------------------------------------------- #
#                          Function Definitions                                #
# ---------------------------------------------------------------------------- #

start_ollama() {
    echo "Starting Ollama service..."
    nohup ollama serve > /ollama.log 2>&1 &
    
    # Wait for Ollama to start up
    echo "Waiting for Ollama to initialize..."
    until curl -s http://localhost:11434/api/version >/dev/null; do
        sleep 1
    done
    
    # Load the model
    echo "Loading openhermes model..."
    ollama run openhermes > /openhermes.log 2>&1 &
    
    # Verify model is ready
    sleep 3
    echo "Available models:"
    ollama list
}

# ---------------------------------------------------------------------------- #
#                               Main Program                                   #
# ---------------------------------------------------------------------------- #

# Start required services
start_ollama

# Run handler
echo "Starting serverless handler..."
python handler.py

# Keep container running (remove if handler runs continuously)
sleep infinity