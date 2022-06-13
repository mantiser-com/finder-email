FROM python

EXPOSE 8080
ENV PYTHONIOENCODING=utf8

RUN pip3 install bs4 requests redis google-search google wp-version-checker mailchimp3 requests firebase_admin pika flask google-api-python-client  nest_asyncio
RUN pip3 install redis-py-cluster maxminddb-geolite2 nats-py
RUN mkdir /code
RUN mkdir /files
COPY . /code/
WORKDIR /code

#Setup gcloud and helm settings
WORKDIR /opt
WORKDIR /code
CMD ["python3","-u","start.py"]
