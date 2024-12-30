import boto3

ec2 = boto3.resource('ec2')
elb = boto3.client('elbv2')
response = elb.create_load_balancer(
    Name='KumarB8LB',
    Subnets=['subnet-01874c4512136bd62','subnet-08fa616f96d54dfc2'],  # Your subnet ID
    SecurityGroups=['sg-01f41ec5b97d3998c'],  # Your security group ID
    Type='application',
    Scheme='internet-facing',
    IpAddressType='ipv4'
)
lb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
