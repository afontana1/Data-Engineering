FROM python:3.10-slim

RUN pip install --no-cache-dir openai

COPY ./examples/ex4/simple_agent.py /app/simple_agent.py

CMD ["python", "/app/simple_agent.py"]