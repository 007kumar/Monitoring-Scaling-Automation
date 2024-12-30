import boto3

# Initialize the Auto Scaling client
asg=boto3.client('autoscaling')

# Replace 'target_group_arn' with the actual ARN of your target group
target_group_arn='arn:aws:elasticloadbalancing:us-east-1:975050024946:targetgroup/KumarB8TG/04492d0b81352fad'

# Create an Auto Scaling group
response=asg.create_auto_scaling_group(
    AutoScalingGroupName='KumarB8ASG',
    LaunchConfigurationName='KumarLaunchConfig',  # Ensure the launch configuration exists
    MinSize=1,
    MaxSize=3,
    DesiredCapacity=1,
    VPCZoneIdentifier='subnet-01874c4512136bd62,subnet-08fa616f96d54dfc2',  # Comma-separated list of subnet IDs in different AZs
    TargetGroupARNs=[target_group_arn],  # Target Group ARN(s)
    HealthCheckType='EC2',  # Health check type, can also be 'ELB'
    HealthCheckGracePeriod=300,  # Time before checking health of instances
    Tags=[
        {
            'Key': 'Name',
            'Value': 'KumarASGInstance',
            'PropagateAtLaunch': True
        }
    ]
)

print('Auto Scaling Group Created:', response)

