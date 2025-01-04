import boto3
import time

# Initialize clients
ec2 = boto3.resource('ec2')
elb = boto3.client('elbv2')
autoscaling = boto3.client('autoscaling')
sns = boto3.client('sns')
s3 = boto3.client('s3')

# Global Variables

BUCKET_NAME = 'kumar08'
ALB_NAME = 'KumarB8LB'
ASG_NAME = 'KumarB8ASG'
LAUNCH_TEMPLATE_NAME = 'KumarLaunchConfig'
SNS_TOPIC_NAME = 'KumarB8Scaling'

def deploy_infrastructure():
    # Step 1: Create S3 Bucket
    
    print("Creating S3 bucket...")
    s3 = boto3.client('s3')
    bucket_name = 'kumar08'
    s3.create_bucket(Bucket=bucket_name)

    # Step 2: Launch EC2 Instance and Configure as Web Server
    
    response = ec2.create_launch_configuration(
        LaunchConfigurationName='KumarLaunchConfig', 
        ImageId='ami-0e2c8caa4b6378d8c', 
        InstanceType='t2.micro', 
        KeyName='jenki', 
        SecurityGroups=['sg-01f41ec5b97d3998c'], 
        AssociatePublicIpAddress=True
    )



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


    # Step 3: Create Application Load Balancer
    response = elb.create_load_balancer(
        Name='KumarB8LB',
        Subnets=['subnet-01874c4512136bd62','subnet-08fa616f96d54dfc2'],
        SecurityGroups=['sg-01f41ec5b97d3998c'],
        Type='application',
        Scheme='internet-facing',
        IpAddressType='ipv4'
    )
    lb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
    print(f"Application Load Balancer '{ALB_NAME}' created.")

    # Step 4: Create Target Group and Register Target

    response = elb.create_target_group(
        Name='KumarB8TG',
        Protocol='HTTP',
        Port=80,
        VpcId='vpc-09f02049d6176fe30',
        TargetType='instance'
    )

    target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
    print(f"Target Group Created with ARN: {target_group_arn}")

    instance_id = 'i-066a8410f3b9d7f66'
    response = elb.register_targets(
        TargetGroupArn=target_group_arn,
        Targets=[{'Id': instance_id}]
    )
    print(f"Instance {instance_id} registered as target.")


    # Step 5: Create Auto Scaling Group

    # ARN of your target group
    target_group_arn='arn:aws:elasticloadbalancing:us-east-1:975050024946:targetgroup/KumarB8TG/04492d0b81352fad'

    # Create an Auto Scaling group
    response=asg.create_auto_scaling_group(
        AutoScalingGroupName='KumarB8ASG',
        LaunchConfigurationName='KumarLaunchConfig',
        MinSize=1,
        MaxSize=3,
        DesiredCapacity=1,
        VPCZoneIdentifier='subnet-01874c4512136bd62,subnet-08fa616f96d54dfc2',
        TargetGroupARNs=[target_group_arn],
        HealthCheckType='EC2',
        HealthCheckGracePeriod=300,
        Tags=[
            {
                'Key': 'Name',
                'Value': 'KumarASGInstance',
                'PropagateAtLaunch': True
            }
        ]
    )

    print('Auto Scaling Group Created:', response)


    # Step 6: Create SNS Topic and Subscription

    response = sns.create_topic(Name='KumarB8Scaling')
    topic_arn = response['TopicArn']

    response = sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint='shiv.rv007@gmail.com'
    )

    # Print the response (for debugging purposes)
    print('Subscription ARN:', response['SubscriptionArn'])


def update_infrastructure():
    print("Updating infrastructure...")
    # Example of updating an Auto Scaling Group's desired capacity
    autoscaling.update_auto_scaling_group(
        AutoScalingGroupName=ASG_NAME,
        DesiredCapacity=2
    )
    print("Auto Scaling Group updated to desired capacity of 2.")


def delete_infrastructure():
    print("Tearing down infrastructure...")
    # Delete Auto Scaling Group
    autoscaling.delete_auto_scaling_group(
        AutoScalingGroupName=ASG_NAME, ForceDelete=True)
    print("Auto Scaling Group deleted.")

    # Delete Launch Configuration
    autoscaling.delete_launch_configuration(
        LaunchConfigurationName=LAUNCH_TEMPLATE_NAME)
    print("Launch Configuration deleted.")

    # Delete Load Balancer and Target Group
    elb.delete_load_balancer(LoadBalancerArn=alb_arn)
    elb.delete_target_group(TargetGroupArn=target_group_arn)
    print("Load Balancer and Target Group deleted.")

    # Delete EC2 instance
    instance.terminate()
    print(f"Terminating EC2 instance {instance.id}...")
    instance.wait_until_terminated()
    print("EC2 instance terminated.")

    # Delete S3 Bucket
    s3.delete_bucket(Bucket=BUCKET_NAME)
    print(f"S3 bucket '{BUCKET_NAME}' deleted.")

    # Delete SNS Topic
    sns.delete_topic(TopicArn=sns_topic_arn)
    print(f"SNS topic '{SNS_TOPIC_NAME}' deleted.")

    print("Infrastructure teardown complete.")


if __name__ == "__main__":
    print("Choose an option:")
    print("1. Deploy Infrastructure")
    print("2. Update Infrastructure")
    print("3. Delete Infrastructure")
    choice = input("Enter your choice: ")

    if choice == '1':
        deploy_infrastructure()
    elif choice == '2':
        update_infrastructure()
    elif choice == '3':
        delete_infrastructure()
    else:
        print("Invalid choice.")

