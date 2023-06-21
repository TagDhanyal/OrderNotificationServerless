import boto3

# boto3 client for sqs
sqs = boto3.client('sqs')

# creating sqs queue
response = sqs.create_queue(QueueName='CustomerOrderInfo')

# get queue url
queue_url = response['QueueUrl']
print(f"Queue URL: {queue_url}")