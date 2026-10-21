@echo off
cd %~dp0
echo Starting FastAPI server from %cd%
python -c "import uvicorn; uvicorn.run('scripts.fastapi_agent:app', reload=True)"
pause 