FROM ubuntu:20.04
MAINTAINER Uned Technolegau Iaith, Prifysgol Bangor University, Language Technologies Unit

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

RUN apt update -q \
 && apt install -y -qq tzdata bash build-essential git curl wget software-properties-common \
    vim ca-certificates libffi-dev libssl-dev libsndfile1 libbz2-dev liblzma-dev locales \
    libboost-all-dev libboost-tools-dev libboost-thread-dev cmake  \
    python python3 python3-pip python3-setuptools python3-dev curl zip zlib1g-dev vim \
    ffmpeg sox alsa-utils \
 && python3 -m pip install --upgrade pip

# Set the locale
RUN locale-gen cy_GB.UTF-8
ENV LANG cy_GB.UTF-8
ENV LANGUAGE cy_GB:en
ENV LC_ALL cy_GB.UTF-8

ARG COQUI_VERSION
ARG MODEL_NAME
ARG MODEL_VERSION

ENV COQUI_VERSION=${COQUI_VERSION}
#ENV MODEL_NAME=${MODEL_NAME}
#ENV MODEL_VERSION=${MODEL_VERSION}

RUN pip3 install stt==$COQUI_VERSION

# Install local Python files and dependencies..
RUN mkdir -p /coqui

WORKDIR /coqui

COPY python/requirements.txt /coqui/
RUN pip3 install -r requirements.txt 

ENV PATH="${PATH}:/coqui"
ENV PYTHONPATH "${PYTHONPATH}:/coqui"

COPY python /coqui/
