FROM ubuntu:18.04

EXPOSE 8080


RUN apt-get update && apt-get install -y python3 python3-pip python3-dev git zlib1g-dev libjpeg-dev libffi-dev telnet curl vim

RUN mkdir /code
RUN mkdir /files
COPY . /code/
WORKDIR /code
RUN pip3 install -r requirements.txt

#Setup gcloud and helm settings
WORKDIR /opt
WORKDIR /code
CMD ["python3","-u","start.py"]