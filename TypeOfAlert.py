import boto3

sns = boto3.client('sns')

# Create SNS topics for different alerts
health_topic_response = sns.create_topic(Name='KumarHealthAlerts')
scaling_topic_response = sns.create_topic(Name='KumarScalingAlerts')
high_traffic_topic_response = sns.create_topic(Name='KumarHighTrafficAlerts')

# Get the Topic ARNs
health_topic_arn = health_topic_response['TopicArn']
scaling_topic_arn = scaling_topic_response['TopicArn']
high_traffic_topic_arn = high_traffic_topic_response['TopicArn']

# Print Topic ARNs
print("Health Topic ARN:", health_topic_arn)
print("Scaling Topic ARN:", scaling_topic_arn)
print("High Traffic Topic ARN:", high_traffic_topic_arn)

# Subscribe to the health alerts topic via email
sns.subscribe(
    TopicArn=health_topic_arn,
    Protocol='email',
    Endpoint='shiv.rv007@gmail.com'
)

# Subscribe to the scaling alerts topic via Email
sns.subscribe(
    TopicArn=scaling_topic_arn,
    Protocol='email',
    Endpoint='shiv.rv007@gmail.com'
)

# Subscribe to the high traffic alerts topic via email
sns.subscribe(
    TopicArn=high_traffic_topic_arn,
    Protocol='email',
    Endpoint='shiv.rv007@gmail.com'
)

response = sns.publish(
    TopicArn=health_topic_arn,  # Make sure health_topic_arn is defined
    Message="Health issue detected!",
    Subject="Health Alert"
)

response = sns.publish(
    TopicArn=scaling_topic_arn,  # Make sure health_topic_arn is defined
    Message="Need Scaling detected!",
    Subject="Need Scaling"
)

response = sns.publish(
    TopicArn=high_traffic_topic_arn,  # Make sure health_topic_arn is defined
    Message="Traffic on Instance detected!",
    Subject="Traffic Alert"
)

