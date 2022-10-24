# docker-coqui-stt-cy

[(cliciwch yma os hoffwch ddarllen y README Cymraeg)](README.md)

 - [Training your own models](#training)
 - [Host a speech recognition server](#speech-recognition-server)


## Training

This repository provides a Docker environment for training **acoustic models** that 
can perform Welsh language speech recognition with the [coqui-stt (version 1.4)](https://github.com/coqui-ai/STT/releases/tag/v1.4.0) libary

This repository also provides a means to train and utilise KenLM based language models that significantly improves recognition results. 

The Welsh language dataset from [Mozilla Common Voice](https://commonvoice.mozilla.org/cy/datasets) is used for training the acoustic model.

This repository also facilitates training and optimizing KenLM language models 
that improve results significantly, especially for a [voice assistant app called
Macsen](http://techiaith.cymru/macsen).

## Speech Recognition server

This repository also contains a simple API server implementation for hosting your trained models locally or online, or for hosting models trained by Bangor University's Language Technologies Unit. 

## Acknowledgements

Welsh speech recognition models would not have been possible without the work and contributions of the following organisations and individuals..

 - Mozilla and everyone who has contributed their voices to [Common Voice](https://commonvoice.mozilla.org/) but in particular to Rhoslyn Prys (meddal.com) who undertook on a voluntary basis a number of crowdsourcing campaigns, to the Mentrau Iaith, Gwynedd Council, the National Library of Wales who worked with Rhoslyn on some of these campaigns, and to the Welsh Government.
 - coqui-stt (https://coqui.ai/code)
 - KenLM : (https://github.com/kpu/kenlm)
 