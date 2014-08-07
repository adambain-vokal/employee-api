FROM python:2.7
RUN apt-get update -qq 
RUN apt-get install -y python2.7-dev libpq-dev socat git postgresql-client-9.3
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
