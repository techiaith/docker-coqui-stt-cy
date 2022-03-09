FROM ghcr.io/coqui-ai/stt-train:v1.2.0

ENV PATH /code/native_client:/usr/local/src/kenlm/build/bin:$PATH
ENV PYTHONPATH $PYTHONPATH:/code/bin/bangor_welsh/egs/shared/python

# Done
WORKDIR /code

# workaround as recommended in https://github.com/coqui-ai/STT/issues/2081 
RUN cp libkenlm.so /usr/lib/
