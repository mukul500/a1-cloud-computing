import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('subscriptions')


def lambda_handler(event, context):
    # Extract email and new_titles from the event
    email = event.get('queryStringParameters', {}).get('email')
    title_to_remove = event.get('queryStringParameters', {}).get('remove')

    response = table.get_item(
        Key={'email': email}
    )

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps("User not found")
        }

    # If the user exists, get the current list of titles and remove the specified title
    current_titles = response['Item']['titles']
    if title_to_remove not in current_titles:
        return {
            'statusCode': 200,
            'body': json.dumps(current_titles)
        }

    current_titles.remove(title_to_remove)

    # Update the item in the table with the updated list of titles
    table.update_item(
        Key={'email': email},
        UpdateExpression='SET titles = :titles',
        ExpressionAttributeValues={':titles': current_titles}
    )

    # Return success message or updated list of titles
    return {
        'statusCode': 200,
        'body': json.dumps(current_titles)
    }