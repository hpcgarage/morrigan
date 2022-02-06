FROM ubuntu:20.04

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

WORKDIR ../morrigan
ENTRYPOINT ./install-morrigan-linux.sh