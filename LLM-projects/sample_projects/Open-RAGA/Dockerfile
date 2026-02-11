FROM python:3.10.11-slim

# Avoid buffering logs
ENV PYTHONUNBUFFERED True


# Install system dependencies (add libmagic here)
RUN apt-get update && apt-get install -y curl libmagic1



# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set working directory and copy app files
ENV APP_HOME /root
WORKDIR $APP_HOME
COPY ./app $APP_HOME/app

# Expose port and run the app
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
