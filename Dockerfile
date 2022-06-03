FROM ubuntu:18.04

EXPOSE 8080
ENV PYTHONIOENCODING=utf8

RUN apt-get update && apt-get install -y python3 python3-pip python3-dev git zlib1g-dev libjpeg-dev libffi-dev telnet curl vim
RUN pip3 install bs4 requests redis google-search google wp-version-checker mailchimp3 requests firebase_admin pika flask google-api-python-client asyncio-nats-client asyncio-nats-streaming nest_asyncio
RUN pip3 install redis-py-cluster maxminddb-geolite2
RUN mkdir /code
RUN mkdir /files
COPY . /code/
WORKDIR /code

#Setup gcloud and helm settings
WORKDIR /opt
WORKDIR /code
CMD ["python3","-u","start.py"]
