FROM amazonlinux:2

RUN yum install -y python37 && \
    yum install -y python3-pip && \
    yum install -y zip && \
    yum clean all

RUN python3.7 -m pip install --upgrade pip && \
    python3.7 -m pip install virtualenv

RUN python3.7 -m venv base

RUN source base/bin/activate
RUN pip install bcrypt cryptography pyjwt -t ./python
RUN pip install cffi -t ./python
RUN pip install stripe -t ./python
COPY ./api_utils/* ./python/api_utils/

RUN zip -r layer.zip ./python/
