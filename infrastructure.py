import json
import pulumi
import pulumi_aws as aws

vpc = aws.ec2.Vpc("nginx-vpc",
    cidr_block="10.0.0.0/16",
    tags={
        "Name": "nginx-vpc",
    })

private_subnets = aws.ec2.Subnet("nginx-private-subnets",
    vpc_id=vpc.id,
    cidr_blocks=["10.0.1.0/24", "10.0.2.0/24"],
    tags={
        "Name": "nginx-private-subnets",
    })

public_subnet = aws.ec2.Subnet("nginx-public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.3.0/24",
    tags={
        "Name": "nginx-public-subnet",
    })

instance_profile = aws.iam.InstanceProfile("nginx-instance-profile",
    role=aws.iam.Role("nginx-instance-role",
        assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Action": ["sts:AssumeRole"],
                "Effect": "Allow",
                "Principal": {"Service": ["ec2.amazonaws.com"]},
            }],
        }),
        policies=[{
            "PolicyName": "nginx-instance-policy",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": ["ec2:Describe*"],
                    "Effect": "Allow",
                    "Resource": "*",
                }],
            },
        }]))

ami = aws.get_ami(most_recent="true",
                 owners=["amazon"],
                 filters=[{
                     "name": "name",
                     "values": ["amzn2-ami-hvm-2.0.*-x86_64-gp2"]
                 }])

launch_config = aws.ec2.LaunchConfiguration("nginx-launch-config",
    instance_type="t2.micro",
    associate_public_ip_address=False,
    iam_instance_profile=instance_profile.name,
    image_id=ami.id)

asg = aws.autoscaling.AutoScalingGroup("nginx-asg",
    launch_configuration=launch_config.id,
    max_size=2,
    min_size=2,
    subnets=private_subnets.id,
    tags=[{
        "Key": "Name",
        "Value": "nginx-asg",
        "PropagateAtLaunch": True,
    }])

lb = aws.elbv2.LoadBalancer("nginx-lb",
    subnets=[public_subnet.id],
    tags={
        "Name": "nginx-lb",
    },
    load_balancer_type="application")
target_group = aws.elbv2.TargetGroup("nginx-target-group",
    port=80,
    protocol="HTTP",
    vpc_id=vpc.id,
    target_type="instance")


# Create a Listener
listener = aws.elbv2.Listener("nginx_listener",
    load_balancer_arn=lb.arn,
    port=80,
    default_action=[{
        "type": "forward",
        "target_group_arn": target_group.arn,
    }])

# Export the Load Balancer's DNS
pulumi.export("lb_dns", lb.dns_name)
