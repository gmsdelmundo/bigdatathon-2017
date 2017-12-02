FROM python:latest

RUN apt-get -y update && \
	apt-get -y upgrade && \
	apt-get install -y build-essential curl

ENV NVM_DIR /usr/local/nvm

RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.6/install.sh | bash

RUN . ${NVM_DIR}/nvm.sh && \
	nvm install v9.2 && \
	nvm use default 

RUN . ${NVM_DIR}/nvm.sh && \
	nvm use default && \
	npm install -g phantomjs-prebuilt --upgrade --unsafe-perm
