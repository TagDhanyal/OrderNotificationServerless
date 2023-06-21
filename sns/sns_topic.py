# run this script before lambda 
import boto3

# Create an SNS client
sns = boto3.client('sns')

# Create a new SNS Topic
response = sns.create_topic(Name='OrderShippedNotificationTopic')

# Get the Topic ARN (Amazon Resource Name)
topic_arn = response['TopicArn']

# Subscribe the first email address
email_1 = 'dhanyalburnertag@gmail.com'
response = sns.subscribe(
    TopicArn=topic_arn,
    Protocol='email',
    Endpoint=email_1
)
subscription_arn_1 = response['SubscriptionArn']

# Subscribe the second email address
email_2 = 'imed.tag@gmail.com' # 
response = sns.subscribe(
    TopicArn=topic_arn,
    Protocol='email',
    Endpoint=email_2
)
subscription_arn_2 = response['SubscriptionArn']

print(f"Created SNS Topic with ARN: {topic_arn}")
print(f"Subscribed {email_1} with ARN: {subscription_arn_1}")
print(f"Subscribed {email_2} with ARN: {subscription_arn_2}")