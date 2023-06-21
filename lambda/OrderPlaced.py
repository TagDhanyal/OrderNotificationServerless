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

# Usage
function_name = 'Customer_order_dateandtime'
role_arn = 'arn:aws:iam::914863377063:role/MyFullLambdaAccessRole2'  # Replace with your IAM role ARN
handler_code = '''
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Queue url
    queue_url = "https://sqs.us-east-2.amazonaws.com/914863377063/CustomerOrderInfo-url"
    
    # Create an SQS client
    sqs = boto3.client('sqs')
    
    # Get the current time in a readable format and send it as a message to the queue
    current_time = datetime.utcnow().isoformat()
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=current_time)
    
    return {
        'statusCode': 200,
        'body': f"Order sent with ID {response['MessageId']}"
    }
'''

function_arn = create_lambda_function(function_name, role_arn, handler_code)
print(f'Lambda function ARN: {function_arn}')