# Order Notification Project

The Order Notification project is a serverless application that enables the processing and notification of order information using AWS services. It utilizes Amazon SQS, Amazon SNS, AWS Lambda, DynamoDB, and API Gateway to facilitate seamless communication, processing, storage, and retrieval of order details.

## Project Overview

The project consists of the following components:

- **SQS Queue**: An Amazon Simple Queue Service (SQS) queue that receives messages.
- **SNS Topic**: An Amazon Simple Notification Service (SNS) topic that allows the publishing of messages.
- **Lambda Function 1: OrderShippedNoti.py**: A Lambda function that triggers on new messages in the SQS queue and publishes them to the SNS topic.
- **Lambda Function 2: lambda_func_db.py**: A Lambda function that is triggered by SNS notifications and stores the message, unique identifier, and timestamp in DynamoDB.
- **DynamoDB Table**: A DynamoDB table that stores the order notification details.
- **API Gateway**: An API Gateway that provides endpoints to create and retrieve orders.

## Project Flow

1. A message containing the current time is sent to the SQS queue.
2. Lambda Function 1 is triggered by the new message in the SQS queue and publishes it to the SNS topic.
3. An email notification is sent to the subscribed email address, containing the current time.
4. Lambda Function 2 is triggered by the SNS notification and stores the message, unique identifier, and timestamp in DynamoDB.
5. Users can create an order by invoking the Create Order API endpoint.
6. The order details are processed and stored in DynamoDB.
7. Users can retrieve the order details by invoking the Get Order API endpoint.

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository to your local machine.
2. Set up the necessary AWS resources:
   - Create an SQS queue and note down its URL.
   - Create an SNS topic and note down its ARN.
   - Create a DynamoDB table named `OrderNotifications` with the required schema.
   - Subscribe to the SNS topic using your desired email address.
3. Configure your AWS credentials on your local machine or your preferred deployment environment.
4. Install the required dependencies using `pip install -r requirements.txt`.
5. Update the following values in the code:
   - Replace `<SQS_QUEUE_URL>` with the URL of your SQS queue.
   - Replace `<SNS_TOPIC_ARN>` with the ARN of your SNS topic.
   - Replace `<DYNAMODB_TABLE_NAME>` with the name of your DynamoDB table.
   - Replace `<CREATE_ORDER_API_URL>` with the API Gateway URL for the Create Order API.
   - Replace `<GET_ORDER_API_URL>` with the API Gateway URL for the Get Order API.
6. Deploy the Lambda functions to AWS Lambda.
7. Configure the SQS queue to trigger Lambda Function 1.
8. Configure the SNS topic to trigger Lambda Function 2.
9. Deploy the API Gateway with the Create Order and Get Order endpoints.
10. Start sending messages to the SQS queue or invoke the Create Order API endpoint to create orders.
11. Invoke the Get Order API endpoint to retrieve order details.

## API Endpoints

The following API endpoints are available:

### Create Order API

- **Endpoint**: `POST /create-order`
- **Description**: Creates a new order.
- **Request Body**: JSON object containing the order details.
- **Request**:
  ```shell
  curl -X POST -H <enter your api-gw>
- **Response**:
  ```json
    {
  "message": "Order created successfully."
    }
### Get Order Details API

- **Endpoint**: `GET /Get-customer-details`
- **Description**: Creates a new order.
- **Request Body**: JSON object containing the order details.
- **Request**:
  ```shell
    curl -X GET -H <enter your api-gw>

- **Response**:
  ```json
  {
  "statusCode": 200,
  "body": "{\"timestamp\": \"2023-06-21T10:30:15Z\", \"notification_id\": \"98765\"}"
  }