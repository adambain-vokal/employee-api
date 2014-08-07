FROM python:2.7
RUN apt-get update -qq && apt-get install -y python2.7-dev libpq-dev
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
