
import boto3

elb = boto3.client('elbv2')

response = elb.create_target_group(
    Name='KumarB8TG',
    Protocol='HTTP',
    Port=80,
    VpcId='vpc-09f02049d6176fe30',  # Replace with your VPC ID
    TargetType='instance'
)

target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
print(f"Target Group Created with ARN: {target_group_arn}")

instance_id = 'i-066a8410f3b9d7f66'  # Replace with the EC2 instance ID you want to register
response = elb.register_targets(
    TargetGroupArn=target_group_arn,
    Targets=[{'Id': instance_id}]
)
print(f"Instance {instance_id} registered as target.")

