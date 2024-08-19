FROM python:3.9-bullseye

WORKDIR /app

# Create the environment:
COPY requirements.txt .

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install -r requirements.txt

# Copy the code, model & streamlit repositories
ADD .streamlit .streamlit
ADD src src
ADD model model

EXPOSE 8501

ENTRYPOINT ["/opt/venv/bin/python", "-m", "streamlit", "run", "src/streamlit.py"]