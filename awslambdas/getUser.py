import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('login')

def lambda_handler(event, context):
    # Extract email from the event
    email = event.get('queryStringParameters', {}).get('email')

    if not email:
        return {
            'statusCode': 400,
            'body': 'Email parameter is missing'
        }

    # Get user from DynamoDB
    response = table.get_item(Key={'email': email})
    user = response.get('Item')

    if not user:
        return {
            'statusCode': 404,
            'body': 'User not found'
        }

    return {
        'statusCode': 200,
        'body': json.dumps(user)
    }