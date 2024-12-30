import boto3

ec2 = boto3.resource('ec2')

user_data_script = '''#!/bin/bash
sudo apt update
sudo apt install -y apache2
sudo systemctl start apache2
sudo systemctl enable apache2
echo "<html><body><h1>Welcome to your web server!</h1></body></html>" > /var/www/html/index.html
'''

instance = ec2.create_instances(
    ImageId='ami-0e2c8caa4b6378d8c',  # Replace with a valid AMI ID
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='jenki',  # Replace with your key pair name
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': True,
            'SubnetId': 'subnet-01874c4512136bd62',  # Replace with your subnet ID
            'DeviceIndex': 0,
            'Groups': ['sg-01f41ec5b97d3998c']  # Security group ID
        }
    ],
    UserData=user_data_script
)

instance_id = instance[0].id
print(f'Launched EC2 instance with ID: {instance_id}')

