import boto3

# Initialize the EC2 client
ec2 = boto3.client('autoscaling')

# Create Launch Configuration
response = ec2.create_launch_configuration(
    LaunchConfigurationName='KumarLaunchConfig', 
    ImageId='ami-0e2c8caa4b6378d8c',  
    InstanceType='t2.micro', 
    KeyName='jenki', 
    SecurityGroups=['sg-01f41ec5b97d3998c'], 
    AssociatePublicIpAddress=True 
)

print('Launch Configuration Created:', response)

