# pulumi-infrastructure-as-code

This repository contains a Pulumi program that sets up a basic infrastructure as code (IaC) solution using AWS. The architecture includes:
- VPC with 2 private and 1 public subnet
- Auto Scaling group with 2 EC2 instances running an nginx Docker container
- Load Balancer in the public subnet that points to the NGINX container

## Requirements

- [Pulumi](https://pulumi.com) installed
- AWS account

## Usage

1. Clone the repository
$ git clone https://github.com/[your-username]/pulumi-infrastructure-as-code.git
