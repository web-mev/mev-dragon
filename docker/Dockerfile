FROM ubuntu:jammy

SHELL ["/bin/bash", "-c"]

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    wget \
    git \
    python3 \
    python3-pip \
    pipx

# Install all software under /opt/software:
RUN mkdir -p /opt/software 
ADD dragon.py /opt/software/ 

ENV PIPX_HOME=/opt/pipx
ENV PIPX_BIN_DIR=/usr/local/bin
ENV PIPX_MAN_DIR=/usr/local/share/man

# Install the NetZoo python library
RUN wget https://github.com/netZoo/netZooPy/archive/refs/tags/0.10.0.tar.gz \
    -P /opt/software && \
    tar xzvf /opt/software/0.10.0.tar.gz -C /opt/software && \
    pipx install -e /opt/software/netZooPy-0.10.0/ 