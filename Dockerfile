# This Dockerfile is used to build an Python environment
FROM python:3.9-slim-bullseye

LABEL maintainer="imgyh<admin@imgyh.com>"

WORKDIR /app

ADD . $WORKDIR

RUN pip3 install -r requirements.txt

CMD ["python3", "TikTokWeb.py"]

