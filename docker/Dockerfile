FROM debian:bullseye

SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    wget \
    git \
    python3 \
    python3-pip

# Install all software under /opt/software:
RUN mkdir -p /opt/software 
ADD dragon.py /opt/software/ 

# Install the NetZoo python library
RUN wget https://github.com/netZoo/netZooPy/archive/refs/tags/0.9.15.tar.gz \
    -P /opt/software && \
    tar xzvf /opt/software/0.9.15.tar.gz -C /opt/software && \
    pip3 install -e /opt/software/netZooPy-0.9.15/ 
    
RUN pip3 install joblib