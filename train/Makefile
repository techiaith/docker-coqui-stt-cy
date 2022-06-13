default: build

# please remember to update COQUI_RELEASE also in the Dockerfile
COQUI_RELEASE := 1.3.0
TECHIAITH_RELEASE := 22.06

build:
	if [ ! -d "checkpoints/coqui" ]; then \
	    mkdir -p checkpoints/coqui; \
	    cd checkpoints/coqui && \
		wget https://github.com/coqui-ai/STT/releases/download/v$(COQUI_RELEASE)/coqui-stt-$(COQUI_RELEASE)-checkpoint.tar.gz && \
		tar xvfz coqui-stt-$(COQUI_RELEASE)-checkpoint.tar.gz && \
		mv coqui-stt-$(COQUI_RELEASE)-checkpoint coqui-en-checkpoint;\
	fi
	if [ ! -d "data/corpws-profi-adnabod-lleferydd" ]; then \
	    mkdir -p data; \
	    cd data && \
	    git clone --branch fersiwn2 https://git.techiaith.bangor.ac.uk/data-porth-technolegau-iaith/corpws-profi-adnabod-lleferydd.git && \
	    cp corpws-profi-adnabod-lleferydd/data/trawsgrifio/clips.csv corpws-profi-adnabod-lleferydd/data/trawsgrifio/clips/; \
	fi
	docker build --rm -t techiaith/coqui-stt-train:v${COQUI_RELEASE} .

run: 
	docker run --gpus all --name techiaith-coqui-train-v${COQUI_RELEASE}-${USER} -it \
		--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
		-v ${PWD}/data/:/data \
		-v ${PWD}/checkpoints/:/checkpoints \
		-v ${PWD}/export/:/export \
		-v ${PWD}/local/:/code/bin/bangor_welsh \
		--env COQUI_RELEASE=${COQUI_RELEASE} \
		--env TECHIAITH_RELEASE=${TECHIAITH_RELEASE} \
		techiaith/coqui-stt-train:v${COQUI_RELEASE} bash


stop:
	-docker stop techiaith-coqui-train-v${COQUI_RELEASE}-${USER}
	-docker rm techiaith-coqui-train-v${COQUI_RELEASE}-${USER}


clean: stop
	-docker rmi techiaith/coqui-stt-train:v${COQUI_RELEASE}
	-docker rmi coqui-ai/coqui-train:v${COQUI_RELEASE}	
	sudo rm -rf checkpoints
