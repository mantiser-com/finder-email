FROM elino/python3

EXPOSE 8080



RUN mkdir /code
RUN mkdir /files
COPY . /code/
WORKDIR /code
RUN pip3 install -r requirements.txt


CMD ["./start.sh"]
