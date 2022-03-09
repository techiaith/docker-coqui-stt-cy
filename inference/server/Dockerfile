FROM ubuntu:20.04

LABEL maintainer="techiaith"
LABEL repository="coqui-stt-cy-server"

ARG COQUI_VERSION
ARG MODEL_NAME
ARG MODEL_VERSION

ENV COQUI_VERSION=${COQUI_VERSION}
ENV MODEL_NAME=${MODEL_NAME}
ENV MODEL_VERSION=${MODEL_VERSION}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

RUN apt update -q \
 && apt install -y -qq tzdata supervisor vim ffmpeg  \
                       python3 python3-pip python3-setuptools python3-dev \
 && python3 -m pip install --upgrade pip

RUN pip3 install stt==$COQUI_VERSION

RUN mkdir -p /stt && \
    mkdir -p /var/log/stt

WORKDIR /stt

COPY python/requirements.txt /stt/
RUN pip3 install -r requirements.txt

COPY python /stt/

EXPOSE 8008

CMD ["/bin/bash", "-c", "/stt/start.sh"]
