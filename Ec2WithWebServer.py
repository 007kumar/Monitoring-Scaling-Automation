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
    ImageId='ami-0e2c8caa4b6378d8c', 
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='jenki',
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': True,
            'SubnetId': 'subnet-01874c4512136bd62', 
            'DeviceIndex': 0,
            'Groups': ['sg-01f41ec5b97d3998c']  
        }
    ],
    UserData=user_data_script
)

instance_id = instance[0].id
print(f'Launched EC2 instance with ID: {instance_id}')

