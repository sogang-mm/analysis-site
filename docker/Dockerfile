FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
		--no-install-recommends \
		git \
		wget \
		python-pip \
		apt-utils && \
	rm -rf /var/lib/apt/lists/*

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN pip install --upgrade pip
RUN pip install setuptools

WORKDIR /workspace
RUN git clone https://github.com/sogang-mm/AnalysisSite.git
WORKDIR /workspace/AnalysisSite
RUN pip install -r requirements.txt

EXPOSE 8000

RUN chmod -R a+w /workspace
