# Stage 1: Build
FROM debian:latest AS builder
ENV DEBIAN_FRONTEND=noninteractive
ARG REPO_URL
ARG REPO_COMMIT

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    golang-go \
    gnupg \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash lazyown
USER lazyown
WORKDIR /home/lazyown

RUN git clone ${REPO_URL} LazyOwn && \
    cd LazyOwn && \
    git checkout ${REPO_COMMIT} && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://repo.charm.sh/apt/gpg.key | gpg --dearmor -o /etc/apt/keyrings/charm.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | tee /etc/apt/sources.list.d/charm.list && \
    apt update && apt install -y gum && \
    ./install.sh && \
    go mod download

# Stage 2: Runtime
FROM debian:latest
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    nmap \
    tmux \
    jq \
    openssl \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash lazyown
USER lazyown
WORKDIR /home/lazyown

COPY --from=builder /home/lazyown/LazyOwn /home/lazyown/LazyOwn
COPY --from=builder /home/lazyown/.local /home/lazyown/.local
COPY entrypoint.sh /home/lazyown/entrypoint.sh

WORKDIR /home/lazyown/LazyOwn
RUN chmod +x /home/lazyown/entrypoint.sh

CMD ["/home/lazyown/entrypoint.sh", "--vpn", "1"]