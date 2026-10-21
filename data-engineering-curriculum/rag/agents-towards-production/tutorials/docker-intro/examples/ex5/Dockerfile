FROM python:3.10-slim

RUN pip install --no-cache-dir openai

COPY ./examples/ex5/dynamic_agent.py /app/dynamic_agent.py

ENV QUESTION="What is the capital of France?"

CMD ["python", "/app/dynamic_agent.py"]