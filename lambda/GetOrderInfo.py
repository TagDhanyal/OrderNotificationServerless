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
function_name = 'GET_customer_details'
role_arn = 'arn:aws:iam::914863377063:role/MyFullLambdaAccessRole2'  # Replace with your IAM role ARN
handler_code = '''
import boto3
import json

def lambda_handler(event, context):
    # Retrieve order details from DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OrderNotifications')
    response = table.get_item(
        Key={
            'notification_id': event['notification_id']
        }
    )
    
    # Extract the order details from the DynamoDB response
    order_details = response.get('Item')
    
    return {
        'statusCode': 200,
        'body': json.dumps(order_details)
    }
'''
function_arn = create_lambda_function(function_name, role_arn, handler_code)
print(f'Lambda function ARN: {function_arn}')