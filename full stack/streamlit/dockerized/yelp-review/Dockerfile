FROM python:3.9.16-slim


COPY . /app

# set working directory as /app
WORKDIR /app

# copy the requirements.txt file to the Docker image
COPY requirements.txt requirements.txt

# use the RUN command to execute the command pip3 install. 
# This works exactly the same as if we were running pip3 install locally on our machine, 
# but this time the modules are installed into the image.
RUN pip3 install -r requirements.txt && \
    pip3 install -e .

# The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime. 
# v1.4 - google cloud run
EXPOSE 8080
CMD streamlit run ./streamlit/app.py --server.port=8080