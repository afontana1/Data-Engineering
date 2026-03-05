FROM apache/airflow:2.5.1
USER root
RUN apt-get update \
  && apt-get install -y git libpq-dev python3 python3-pip \
  && apt-get install -y openjdk-11-jdk \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

COPY Dockerfiles/requirements.txt .
USER airflow
RUN pip3 install -r requirements.txt

