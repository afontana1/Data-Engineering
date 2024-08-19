@echo off

set DOCKER_IMAGE_NAME="rest-app"

REM Check if the Docker image exists
docker images -q %DOCKER_IMAGE_NAME% > nul 2>&1
if %errorlevel% neq 0 (
    echo Docker image not found. Building...
    
    REM Build the Docker image
    docker build -t %DOCKER_IMAGE_NAME% .
    if %errorlevel% neq 0 (
        echo Docker image build failed.
        exit /b 1
    )
) else (
    echo Docker image found.
)

REM Run the Docker container
docker run -it %DOCKER_IMAGE_NAME%