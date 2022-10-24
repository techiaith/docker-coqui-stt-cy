FROM ghcr.io/coqui-ai/stt-train:v1.4.0

RUN apt update -q \
 && apt install -y -qq libboost-program-options-dev libboost-thread-dev

ENV PATH /code/native_client:/usr/local/src/kenlm/build/bin:$PATH
ENV PYTHONPATH $PYTHONPATH:/code/bin/bangor_welsh/egs/shared/python

# Done
WORKDIR /code

ADD local/egs/shared/python/requirements.txt .
RUN python3 -m pip install -r requirements.txt


# workaround as recommended in https://github.com/coqui-ai/STT/issues/2081 
RUN cp libkenlm.so /usr/lib/
