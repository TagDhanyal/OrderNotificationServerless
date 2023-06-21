# I know that its not best practice to use full access this is just a test/dev enviroment

import boto3

def create_iam_role(role_name):
    # Create an IAM client
    iam_client = boto3.client('iam')

    # Create the IAM role
    response = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument='''{
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }]
        }'''
    )

    # Attach policies for full access to SQS, SNS, and API Gateway
    policies = [
        'arn:aws:iam::aws:policy/AmazonSQSFullAccess',
        'arn:aws:iam::aws:policy/AmazonSNSFullAccess',
        'arn:aws:iam::aws:policy/AmazonAPIGatewayAdministrator',
        'arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess'
    ]

    for policy_arn in policies:
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )

    return response['Role']['Arn']

# Usage
role_name = 'MyFullLambdaAccessRole2'

role_arn = create_iam_role(role_name)
print(f'IAM Role ARN: {role_arn}')