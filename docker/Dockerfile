FROM ubuntu:16.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
	   git wget python-pip apt-utils \
	&& rm -rf /var/lib/apt/lists/*

ENV DOCKERIZE_VERSION v0.6.1
RUN wget -q https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN pip install --upgrade pip
RUN pip install setuptools

WORKDIR /workspace
RUN git clone https://github.com/sogang-mm/Analysis-Site.git
WORKDIR /workspace/Analysis-Site
RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

RUN chmod -R a+w /workspace

EXPOSE 8000
