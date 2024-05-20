ARG BASE_IMAGE=ubuntu:20.04

FROM ${BASE_IMAGE}

#ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:-compute,utility}

RUN apt update && \
    apt install -y \
        wget build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev \
        libreadline-dev libffi-dev libsqlite3-dev libbz2-dev liblzma-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get install -y tcl

RUN apt-get -y install git
RUN apt-get install -y ffmpeg

ARG PYTHON_VERSION=3.9.12

RUN cd /tmp && \
    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make && make install && \
    cd .. && rm Python-${PYTHON_VERSION}.tgz && rm -r Python-${PYTHON_VERSION} && \
    ln -s /usr/local/bin/python3 /usr/local/bin/python && \
    ln -s /usr/local/bin/pip3 /usr/local/bin/pip && \
    python -m pip install --upgrade pip && \
    rm -r /root/.cache/pip

ARG PYTORCH_VERSION=2.0.0
#ARG PYTORCH_VERSION_SUFFIX=+cpu
ARG TORCHVISION_VERSION=0.15.0
#ARG TORCHVISION_VERSION_SUFFIX=+cpu
ARG TORCHAUDIO_VERSION=2.0.0
#ARG TORCHAUDIO_VERSION_SUFFIX=+cpu
ARG PYTORCH_DOWNLOAD_URL=https://download.pytorch.org/whl/cu118/torch_stable.html

RUN if [ ! $TORCHAUDIO_VERSION ]; \
    then \
        TORCHAUDIO=; \
    else \
        TORCHAUDIO=torchaudio==${TORCHAUDIO_VERSION}${TORCHAUDIO_VERSION_SUFFIX}; \
    fi && \
    if [ ! $PYTORCH_DOWNLOAD_URL ]; \
    then \
        pip install \
            torch==${PYTORCH_VERSION}${PYTORCH_VERSION_SUFFIX} \
            torchvision==${TORCHVISION_VERSION}${TORCHVISION_VERSION_SUFFIX} \
            ${TORCHAUDIO}; \
    else \
        pip install \
            torch==${PYTORCH_VERSION}${PYTORCH_VERSION_SUFFIX} \
            torchvision==${TORCHVISION_VERSION}${TORCHVISION_VERSION_SUFFIX} \
            ${TORCHAUDIO} \
            -f ${PYTORCH_DOWNLOAD_URL}; \
    fi && \
    rm -r /root/.cache/pip

WORKDIR /workspace

ADD requirements.txt .
RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

ADD . /workspace

CMD ["python3.9", "main.py"]
# RUN python3.9 main.py
