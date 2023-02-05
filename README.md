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
```
$ git clone https://github.com/[your-username]/pulumi-infrastructure-as-code.git
```
2. Change to the directory and install the required dependencies
```
$ cd pulumi-infrastructure-as-code
$ pulumi plugin install resource aws v2.17.2
```
3. Create a new stack and configure the AWS credentials
```
$ pulumi stack init
$ pulumi config set aws:region [your-region]
$ pulumi config set aws:profile [your-profile]
```
4. Run the Pulumi program
```
$ pulumi up
```
5. Once the deployment is complete, the Load Balancer's DNS will be displayed as the output. Open it in the browser to access the NGINX welcome page.
