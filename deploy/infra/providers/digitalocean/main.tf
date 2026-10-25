terraform {
  required_version = ">= 1.5.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

variable "region" {
  description = "DigitalOcean region slug"
  type        = string
  default     = "nyc1"
}

variable "droplet_size" {
  description = "Droplet size for the ephemeral C2"
  type        = string
  default     = "s-1vcpu-1gb"
}

variable "ssh_key_name" {
  description = "Existing DO SSH key name for operator access"
  type        = string
  default     = ""
}

data "digitalocean_ssh_key" "operator" {
  count = var.ssh_key_name != "" ? 1 : 0
  name  = var.ssh_key_name
}

resource "digitalocean_droplet" "c2" {
  image    = "docker-22-04"
  name     = "lazyown-c2-ephemeral"
  region   = var.region
  size     = var.droplet_size
  ssh_keys = var.ssh_key_name != "" ? [data.digitalocean_ssh_key.operator[0].id] : []
  tags     = ["lazyown", "ephemeral", "c2"]

  user_data = file("${path.module}/cloud-init.yaml")
}

resource "digitalocean_droplet" "redirector" {
  image    = "docker-22-04"
  name     = "lazyown-redirector-ephemeral"
  region   = var.region
  size     = "s-1vcpu-1gb"
  ssh_keys = var.ssh_key_name != "" ? [data.digitalocean_ssh_key.operator[0].id] : []
  tags     = ["lazyown", "ephemeral", "redirector"]

  user_data = file("${path.module}/cloud-init.yaml")
}

resource "digitalocean_firewall" "c2" {
  name = "lazyown-c2-ephemeral"

  droplet_ids = [
    digitalocean_droplet.c2.id,
    digitalocean_droplet.redirector.id,
  ]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "4444"
    source_addresses = ["${digitalocean_droplet.redirector.ipv4_address}/32"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

output "c2_ip" {
  value = digitalocean_droplet.c2.ipv4_address
}

output "redirector_ip" {
  value = digitalocean_droplet.redirector.ipv4_address
}
