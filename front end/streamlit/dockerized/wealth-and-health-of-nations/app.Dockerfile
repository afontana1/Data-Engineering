#The FROM command tells Docker to create a base layer.
#In this case, we have used the Python v3.10 image available in Docker Hub
# as the base image on which our application will be built
FROM python:3.10
# COPY command is duplicating the local requirements.txt file (which contains package names and versions
# required by the model app) into the Docker image’s ‘app’ folder
COPY requirements.txt app/requirements.txt
# WORKDIR sets the Working Directory within the Docker image.
# In this case, it is creating an 'app' folder where all files will be stored
WORKDIR /app
# The RUN command specifies what Command Line Interface (CLI) commands to run within the Docker container.
# In this Dockerfile, it is installing all packages and dependencies in the requirements.txt file,
# and running some additional commands to download the spaCy ‘en_core_web_sm’ model correctly from the web
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# COPY command is duplicating all local files into the Docker image’s ‘app’ folder
COPY . /app
# EXPOSE specifies the port number on the network where our application will be deployed and accessible.
# The Streamlit library is particularly compatible with the Port 8501 as set above
EXPOSE 8501
# CMD is used to specify the commands to be run when the Docker container is started
CMD streamlit run main.py
