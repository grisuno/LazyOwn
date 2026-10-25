FROM python:3.12-slim-bookworm AS builder
ENV DEBIAN_FRONTEND=noninteractive
ARG REPO_URL
ARG REPO_COMMIT

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        gnupg \
        golang-go \
        build-essential && \
    curl -fsSL https://github.com/charmbracelet/gum/releases/download/v0.14.5/gum_0.14.5_amd64.deb \
        -o /tmp/gum.deb && \
    dpkg -i /tmp/gum.deb && \
    rm -f /tmp/gum.deb && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash lazyown
USER lazyown
WORKDIR /home/lazyown

RUN git clone "${REPO_URL}" LazyOwn && \
    cd LazyOwn && \
    git checkout "${REPO_COMMIT}" && \
    python3 -m venv env && \
    . env/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    if [ -f requirements.txt ]; then \
        sed -i '/^certipy-ad==/d' requirements.txt && \
        grep -v '^#' requirements.txt | grep -v '^$' | xargs -r -n 50 pip install --no-cache-dir --no-deps && \
        pip install --no-cache-dir --no-deps certipy-ad==5.0.4 && \
        pip install --no-cache-dir bleach; \
    fi && \
    if [ -f go.mod ]; then go mod download; fi

COPY --chown=lazyown:lazyown hostdiscover.sh /home/lazyown/LazyOwn/modules/hostdiscover.sh

FROM python:3.12-slim-bookworm
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        iproute2 \
        iputils-ping \
        jq \
        net-tools \
        nmap \
        openssl \
        parallel \
        tmux && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash lazyown && \
    mkdir -p /home/lazyown/LazyOwn/sessions /home/lazyown/LazyOwn/sessions/logs && \
    ln -sf /home/lazyown/payload.json /home/lazyown/LazyOwn/payload.json

COPY --from=builder --chown=lazyown:lazyown /home/lazyown/LazyOwn /home/lazyown/LazyOwn
COPY --chown=lazyown:lazyown entrypoint.sh /home/lazyown/entrypoint.sh
RUN chmod +x /home/lazyown/entrypoint.sh && \
    chown -R lazyown:lazyown /home/lazyown

USER lazyown
WORKDIR /home/lazyown/LazyOwn

CMD ["/home/lazyown/entrypoint.sh", "--vpn", "1"]
