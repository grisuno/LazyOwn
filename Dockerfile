# LazyOwn production Docker image
# Multi-platform: linux/amd64, linux/arm64
# Usage: docker pull ghcr.io/grisuno/lazyown:latest
#        docker run -it --rm -v "$(pwd)/payload.json:/app/payload.json" ghcr.io/grisuno/lazyown

FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/grisuno/LazyOwn"
LABEL org.opencontainers.image.description="LazyOwn RedTeam Framework"
LABEL org.opencontainers.image.licenses="GPL-3.0-only"

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    curl \
    jq \
    git \
    openssl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

WORKDIR /app

COPY . .

RUN useradd -m -s /bin/bash lazyown && \
    mkdir -p /app/sessions /app/profiles && \
    chown -R lazyown:lazyown /app

USER lazyown

ENTRYPOINT ["python3", "-W", "ignore", "lazyown.py"]
