FROM debian:bookworm-slim AS builder
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
        python3 \
        python3-pip \
        python3-venv \
        build-essential && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://repo.charm.sh/apt/gpg.key \
        | gpg --dearmor -o /etc/apt/keyrings/charm.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" \
        > /etc/apt/sources.list.d/charm.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends gum && \
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
        pip install --no-cache-dir -r requirements.txt; \
    fi && \
    if [ -f go.mod ]; then go mod download; fi

FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        jq \
        nmap \
        openssl \
        python3 \
        python3-pip \
        python3-venv \
        tmux && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash lazyown

COPY --from=builder --chown=lazyown:lazyown /home/lazyown/LazyOwn /home/lazyown/LazyOwn
COPY --chown=lazyown:lazyown entrypoint.sh /home/lazyown/entrypoint.sh
RUN chmod +x /home/lazyown/entrypoint.sh

USER lazyown
WORKDIR /home/lazyown/LazyOwn

CMD ["/home/lazyown/entrypoint.sh", "--vpn", "1"]
