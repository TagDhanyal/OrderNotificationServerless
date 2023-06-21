import boto3

def create_lambda_function(function_name, role_arn, handler_code):
    # Create a Lambda client
    lambda_client = boto3.client('lambda')
    
    # Create the Lambda function
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.8',
        Role=role_arn,
        Handler='lambda_handler',
        Code={
            'ZipFile': handler_code.encode()
        },
        Description='Lambda function for sending messages to an SQS queue',
        Timeout=30,
        MemorySize=128,
        Publish=True
    )
    
    return response['FunctionArn']

def create_event_source_mapping(function_name, sqs_queue_arn):
    # Create an AWS Lambda client
    lambda_client = boto3.client('lambda')

    # Create the event source mapping
    response = lambda_client.create_event_source_mapping(
        FunctionName=function_name,
        EventSourceArn=sqs_queue_arn,
        Enabled=True,
        BatchSize=10,  # The number of messages to retrieve in each batch
        StartingPosition='LATEST'  # Start consuming messages from the latest available/ Best practice to use a version
    )

    return response['UUID']

function_name = 'OrderShippedNotification'
role_arn = ''  # Replace with your IAM role ARN
handler_code = '''
# Initialize the SNS client
import boto3
sns = boto3.client('sns')

# SNS Topic ARN 
sns_topic_arn = "arn:aws:sns:us-east-2:914863377063:OrderShippedNotificationTopic" #

def lambda_handler(event, context):
    # Get the SQS message from the Lambda event
    sqs_message = event['Records'][0]['body']

    # Publish the SQS message to the SNS Topic
    sns.publish(TopicArn=sns_topic_arn, Message=sqs_message)

    return {
        'statusCode': 200,
        'body': 'SQS message forwarded to the SNS Topic.'
    }
'''

# Create the Lambda function
function_arn = create_lambda_function(function_name, role_arn, handler_code)
print(f'Lambda function ARN: {function_arn}')

# Set up the event source mapping with SQS
sqs_queue_arn ='arn:aws:sqs:us-east-2:914863377063:CustomerOrderInfo'  # Replace with your SQS queue ARN
event_mapping_uuid = create_event_source_mapping(function_name, sqs_queue_arn)
print(f'Event source mapping UUID: {event_mapping_uuid}')