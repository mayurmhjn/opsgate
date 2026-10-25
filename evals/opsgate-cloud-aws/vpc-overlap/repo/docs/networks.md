# Networks

| Network | CIDR | Notes |
|---------|------|-------|
| On-prem data center | 10.0.0.0/12 | Reached over Site-to-Site VPN |
| Dev VPC (AWS, eu-west-1) | 10.20.0.0/16 | |
| Staging VPC (AWS, eu-west-1) | 10.21.0.0/16 | |
| Partner VPN (logistics provider) | 172.16.0.0/16 | Their side, cannot change |
| Office Wi-Fi | 192.168.0.0/16 | |

Plan: production must reach on-prem and the partner network through a Transit Gateway next quarter.
