default: build


config:	
	$(eval COQUI_VERSION = 1.2.0)
	$(eval MODEL_NAME = macsen)
	$(eval MODEL_VERSION = 22.02)
	$(eval PORT_NUMBER = 5505)


build: config
	if [ ! -d "models/${MODEL_NAME}" ]; then \
        mkdir -p models/${MODEL_NAME}; \
        cd models/${MODEL_NAME} && \
	    #wget https://github.com/techiaith/docker-coqui-stt-cy/releases/download/${MODEL_VERSION}/techiaith_bangor_${MODEL_VERSION}.tflite;\
	    #wget https://github.com/techiaith/docker-coqui-stt-cy/releases/download/${MODEL_VERSION}/techiaith_bangor_${MODEL_NAME}_${MODEL_VERSION}.scorer;\
		wget http://lwk1900002.ad.bangor.ac.uk/stt/techiaith_bangor_${MODEL_VERSION}.tflite;\
	    wget http://lwk1900002.ad.bangor.ac.uk/stt/techiaith_bangor_${MODEL_NAME}_${MODEL_VERSION}.scorer;\
    fi
	docker build --rm -t techiaith/coqui-stt-${COQUI_VERSION}-server:${MODEL_NAME}_${MODEL_VERSION} \
		--build-arg COQUI_VERSION=${COQUI_VERSION} \
		--build-arg MODEL_NAME=${MODEL_NAME} \
		--build-arg MODEL_VERSION=${MODEL_VERSION} \
		.


run: config
	mkdir -p ${PWD}/log/
	mkdir -p ${PWD}/recordings/
	docker run --name techiaith-coqui-stt-${COQUI_VERSION}-server_${MODEL_NAME}-${MODEL_VERSION} \
		--restart=always \
		-it -d -p ${PORT_NUMBER}:8008 \
		-v ${PWD}/models/:/models \
		-v ${PWD}/recordings/:/recordings \
		-v ${PWD}/log/:/var/log/stt \
		techiaith/coqui-stt-${COQUI_VERSION}-server:${MODEL_NAME}_${MODEL_VERSION}


bash: config
	docker exec -it techiaith-coqui-stt-${COQUI_VERSION}-server_${MODEL_NAME}-${MODEL_VERSION} bash


stop: config
	-docker stop techiaith-coqui-stt-${COQUI_VERSION}-server_${MODEL_NAME}-${MODEL_VERSION}
	-docker rm techiaith-coqui-stt-${COQUI_VERSION}-server_${MODEL_NAME}-${MODEL_VERSION}
	rm -rf ${PWD}/log


clean: config stop
	-docker rmi techiaith/coqui-stt-${COQUI_VERSION}-server:${MODEL_NAME}_${MODEL_VERSION}


test: config
	curl -F 'soundfile=@question.wav' http://localhost:${PORT_NUMBER}/speech_to_text/
