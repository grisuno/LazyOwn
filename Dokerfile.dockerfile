FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    openssl \
    ca-certificates \
    python3-dev \
    build-essential \
    wget \
    git \
    && \
    rm -fr /var/lib/apt/lists/*

RUN git clone https://github.com/grisuno/LazyOwn.git

WORKDIR LazyOwn

COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN ./install.sh
EXPOSE 80 4444
CMD ["bash", "fast_run_as_r00t.sh --vpn 1"]