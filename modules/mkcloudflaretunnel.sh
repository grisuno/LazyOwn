#!/bin/bash
# cloudflare_tunnel.sh - Download cloudflared and create a tunnel to localhost on a specified port.
gum log --time rfc822 --level info "    [+] Start the tunnel."
gum spin --spinner dot --title "Disposable tunneling..." -- sleep 1
if command -v gum &> /dev/null; then
    gum spin --spinner dot --title "Gum is installed..." -- sleep 0.1
else
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://repo.charm.sh/apt/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg
    echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | sudo tee /etc/apt/sources.list.d/charm.list
    sudo apt update && sudo apt install gum
fi

if [ -z "$1" ]; then
    gum style \
	--foreground 212 --border-foreground 212 --border double \
	--align center --width 50 --margin "1 2" --padding "2 4" \
	"Usage: $0 <port>"
  exit 1
fi

port=$1

if [ ! -f "cloudflared" ]; then
    gum log --time rfc822 --level info "    [+] Downloading the binary."
    gum style \
    --foreground 212 --border-foreground 212 --border double \
    --align center --width 50 --margin "1 2" --padding "2 4" \
    "Downloading cloudflared..."
    arch=$(uname -m)
    os=$(uname -s)

  if [[ "$os" == "Linux" ]]; then
    if [[ "$arch" == *'arm'* ]]; then
        gum spin --spinner dot --title "Downloading..." -- wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm -O cloudflared
    elif [[ "$arch" == *'aarch64'* ]]; then
        gum spin --spinner dot --title "Downloading..." -- wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -O cloudflared
    elif [[ "$arch" == *'x86_64'* ]]; then
        gum spin --spinner dot --title "Downloading..." -- wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
    elif [[ "$arch" == *'i686'* ]]; then
        gum spin --spinner dot --title "Downloading..." -- wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386 -O cloudflared
    else
        gum style \
    	--foreground 212 --border-foreground 212 --border double \
    	--align center --width 50 --margin "1 2" --padding "2 4" \
    	"Unsupported architecture for automatic download. Please download cloudflared manually from https://github.com/cloudflare/cloudflared/releases/"
        exit 1
    fi
  elif [[ "$os" == "Darwin" ]]; then
    gum spin --spinner dot --title "Downloading..." -- wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz -O cloudflared.tgz
    gum spin --spinner dot --title "Tar..." -- tar -zxvf cloudflared.tgz
    rm cloudflared.tgz
  else
    gum style \
	--foreground 212 --border-foreground 212 --border double \
	--align center --width 50 --margin "1 2" --padding "2 4" \
	"Unsupported operating system for automatic download. Please download cloudflared manually from https://github.com/cloudflare/cloudflared/releases/"
    exit 1
  fi
  gum log --time rfc822 --level info "    [+] Doing the magic."
  gum spin --spinner dot --title "Chmoding..." -- chmod +x cloudflared
  gum style \
	--foreground 212 --border-foreground 212 --border double \
	--align center --width 50 --margin "1 2" --padding "2 4" \
	"Cloudflared downloaded."
else
    gum style \
	--foreground 212 --border-foreground 212 --border double \
	--align center --width 50 --margin "1 2" --padding "2 4" \
	"Cloudflared already exists."
fi
gum log --time rfc822 --level info "    [+] Starting the tunnel."
gum style \
	--foreground 212 --border-foreground 212 --border double \
	--align center --width 50 --margin "1 2" --padding "2 4" \
	"Starting Cloudflare tunnel for port $port using HTTPS with TLS verification disabled..."
./cloudflared tunnel -url "https://localhost:$port" --no-tls-verify  --logfile cf.log

gum style \
	--foreground 212 --border-foreground 212 --border double \
	--align center --width 50 --margin "1 2" --padding "2 4" \
	"Cloudflare tunnel is running. Press Ctrl+C to stop."
gum log --time rfc822 --level info "    [+] End the tunnel."
