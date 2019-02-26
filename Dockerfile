FROM ubuntu:latest

MAINTAINER Caroline "goldiesilber23@gmail.com"

EXPOSE 8080
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

COPY /app /
WORKDIR /

RUN pip install -r requirements.txt

CMD [ "gunicorn", "-c", "gunicorn.conf", "app:app" ]
