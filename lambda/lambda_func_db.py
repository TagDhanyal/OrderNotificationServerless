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
        Description='Lambda function triggered by SNS messages',
        Timeout=30,
        MemorySize=128,
        Publish=True
    )
    
    return response['FunctionArn']

# Usage
function_name = 'SNSNotificationHandler'
role_arn = 'arn:aws:iam::914863377063:role/MyFullLambdaAccessRole2'  # Replace with your IAM role ARN
handler_code = '''
import json
import uuid
from datetime import datetime

def lambda_handler(event, context):
    # Extract the current time from the SNS event (without parsing as JSON as my initial SNS message is not in JSON format)
    message = event['Records'][0]['Sns']['Message']

    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OrderNotifications')

    # Generate a unique identifier and timestamp
    notification_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    # Store the data in the DynamoDB table
    table.put_item(
        Item={
            'notification_id': notification_id,
            'timestamp': timestamp,
            'message': message
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully saved SNS message: {notification_id}')
    }
'''

# Create the Lambda function
function_arn = create_lambda_function(function_name, role_arn, handler_code)
print(f'Lambda function ARN: {function_arn}')

# Configure the SNS trigger
sns_client = boto3.client('sns')
sns_topic_arn = 'arn:aws:sns:us-east-2:914863377063:OrderShippedNotificationTopic'  # Replace with your SNS topic ARN
sns_client.subscribe(
    TopicArn=sns_topic_arn,
    Protocol='lambda',
    Endpoint=function_arn
)