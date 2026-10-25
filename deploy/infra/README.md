# Infra (IaC)

Ephemeral infrastructure as code. Local Docker by default, Terraform for
billable cloud resources.

## Layout

| Path | Purpose |
|------|---------|
| `providers/digitalocean/` | Droplets + firewall for C2 and redirector |
| `../c2/` | Local C2 stack with automatic TLS |
| `../redirector/` | Disposable cloudflared redirectors |

## Usage

```bash
infra deploy --provider local
infra deploy --provider digitalocean --region nyc1
infra destroy --provider digitalocean
```

Set `DIGITALOCEAN_TOKEN` before any cloud deploy. Always `destroy` at the
end of the campaign.
