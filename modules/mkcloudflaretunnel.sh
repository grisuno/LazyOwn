#!/bin/bash
# cloudflare_tunnel.sh - Download cloudflared and create a tunnel to localhost on a specified port.

if [ -z "$1" ]; then
  echo "Usage: $0 <port>"
  exit 1
fi

port=$1

if [ ! -f "cloudflared" ]; then
  echo "Downloading cloudflared..."
  arch=$(uname -m)
  os=$(uname -s)

  if [[ "$os" == "Linux" ]]; then
    if [[ "$arch" == *'arm'* ]]; then
      wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm -O cloudflared
    elif [[ "$arch" == *'aarch64'* ]]; then
      wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -O cloudflared
    elif [[ "$arch" == *'x86_64'* ]]; then
      wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
    elif [[ "$arch" == *'i686'* ]]; then
      wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386 -O cloudflared
    else
      echo "Unsupported architecture for automatic download. Please download cloudflared manually from https://github.com/cloudflare/cloudflared/releases/"
      exit 1
    fi
  elif [[ "$os" == "Darwin" ]]; then
    wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz -O cloudflared.tgz
    tar -zxvf cloudflared.tgz
    rm cloudflared.tgz
  else
    echo "Unsupported operating system for automatic download. Please download cloudflared manually from https://github.com/cloudflare/cloudflared/releases/"
    exit 1
  fi
  chmod +x cloudflared
  echo "Cloudflared downloaded."
else
  echo "Cloudflared already exists."
fi

echo "Starting Cloudflare tunnel for port $port using HTTPS with TLS verification disabled..."
./cloudflared tunnel -url "https://localhost:$port" --no-tls-verify  --logfile cf.log 

echo "Cloudflare tunnel is running. Press Ctrl+C to stop."