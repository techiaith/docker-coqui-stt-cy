default: build

# --- Runtime with Python REST API  ----------------------------------------------------

$(eval COQUI_VERSION = 1.2.0)

#$(eval DEFAULT_MODEL = macsen)
$(eval DEFAULT_MODEL = transcribe)

#config-macsen: 
#	$(eval MODEL_NAME = macsen)
#	$(eval MODEL_VERSION= 21.03)
#	$(eval PORT_NUMBER = 5503)

config-transcribe: 
	$(eval MODEL_NAME = transcribe)
	$(eval MODEL_VERSION = 22.02)
	$(eval PORT_NUMBER = 5501)



build: config-${DEFAULT_MODEL}
	if [ ! -d "data/corpws-profi-adnabod-lleferydd" ]; then \
	    mkdir -p data; \
	    cd data && git clone https://git.techiaith.bangor.ac.uk/data-porth-technolegau-iaith/corpws-profi-adnabod-lleferydd.git; \
	fi
	docker build --rm -t techiaith/coqui-${COQUI_VERSION}-evaluation \
		--build-arg COQUI_VERSION=${COQUI_VERSION} \
		--build-arg MODEL_NAME=${MODEL_NAME} \
		--build-arg MODEL_VERSION=${MODEL_VERSION} \
		.


run: config-${DEFAULT_MODEL}
	docker run --name coqui-${COQUI_VERSION}-evaluation-${USER} --restart=always \
		-it \
		-v ${PWD}/../../train/export/:/coqui/models \
		-v ${PWD}/data/:/data \
		techiaith/coqui-${COQUI_VERSION}-evaluation
		bash

stop: config-${DEFAULT_MODEL}
	-docker stop coqui-${COQUI_VERSION}-evaluation-${USER}
	-docker rm coqui-${COQUI_VERSION}-evaluation-${USER}

clean: stop 
	-docker rmi techiaith/coqui-${COQUI_VERSION}-evaluation
 
