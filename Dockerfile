FROM ubuntu:latest

MAINTAINER Caroline "goldiesilber23@gmail.com"

EXPOSE 8080
RUN apt-get update -y

COPY /app /
WORKDIR /

RUN pip install -r requirements.txt

CMD [ "gunicorn", "-c", "gunicorn.conf", "app:app" ]
