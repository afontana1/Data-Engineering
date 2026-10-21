"""
Simple script to run the FastAPI server from the correct directory
"""
import os
import sys
import subprocess

# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change to the directory containing the script
os.chdir(script_dir)

# Run uvicorn with the correct module path
print("Starting FastAPI server...")
print(f"Current directory: {os.getcwd()}")
print("Running: uvicorn scripts.fastapi_agent:app --reload")

try:
    subprocess.run(["uvicorn", "scripts.fastapi_agent:app", "--reload"], check=True)
except Exception as e:
    print(f"Error running server: {e}")
    sys.exit(1) 