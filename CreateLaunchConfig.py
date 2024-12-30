import boto3

# Initialize the EC2 client
ec2 = boto3.client('autoscaling')

# Create Launch Configuration
response = ec2.create_launch_configuration(
    LaunchConfigurationName='KumarLaunchConfig',  # Name of your Launch Configuration
    ImageId='ami-0e2c8caa4b6378d8c',  # AMI ID (use a valid AMI ID for your region)
    InstanceType='t2.micro',  # Instance type
    KeyName='jenki',  # Name of the EC2 Key Pair
    SecurityGroups=['sg-01f41ec5b97d3998c'],  # List of security group IDs
    AssociatePublicIpAddress=True  # Optional: Enable public IP assignment
)

print('Launch Configuration Created:', response)

