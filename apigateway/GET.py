import boto3

def create_api_gateway_trigger(api_name, lambda_function_arn, lambda_function_name):
    # Create an API Gateway client
    apigateway_client = boto3.client('apigateway')
    
    # Create a new REST API
    api_response = apigateway_client.create_rest_api(
        name=api_name,
        description='API Gateway Trigger for Lambda Function',
        endpointConfiguration={'types': ['REGIONAL']}
    )
    
    # Retrieve the API ID
    api_id = api_response['id']
    
    # Create a new resource under the API
    resource_response = apigateway_client.create_resource(
        restApiId=api_id,
        parentId=api_response['rootResourceId'],
        pathPart='{proxy+}'
    )
    
    # Retrieve the resource ID
    resource_id = resource_response['id']
    
    # Create a new method for the resource
    apigateway_client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='GET',
        authorizationType='NONE'
    )
    
    # Set the Lambda function as the integration for the method
    apigateway_client.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='GET',
        integrationHttpMethod='POST',
        type='AWS_PROXY',
        uri=f'arn:aws:apigateway:{boto3.session.Session().region_name}:lambda:path/2015-03-31/functions/{lambda_function_arn}/invocations'
    )
    
    # Create a deployment for the API
    apigateway_client.create_deployment(
        restApiId=api_id,
        stageName='dev'
    )
    # Return the API Gateway invoke URL
    return f'https://{api_id}.execute-api.{boto3.session.Session().region_name}.amazonaws.com/prod/'

# Usage
api_name = 'Get_customer_details'
lambda_function_arn = '' # enter lambda function ARN < GetOrderInfo.py >
lambda_function_name = 'GET_customer_details'

invoke_url = create_api_gateway_trigger(api_name, lambda_function_arn, lambda_function_name)
print(f'API Gateway Invoke URL: {invoke_url}')