import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('subscriptions')


def lambda_handler(event, context):
    # Extract email and new_titles from the event
    email = event.get('queryStringParameters', {}).get('email')
    new_title = event.get('queryStringParameters', {}).get('new_title')

    # Get the current list of titles for the user
    response = table.get_item(
        Key={'email': email}
    )

    if 'Item' not in response:
        # If the user doesn't exist, create a new item with the new title
        table.put_item(
            Item={'email': email, 'titles': [new_title]}
        )
        return {
            'statusCode': 200,
            'body': json.dumps([new_title])
        }

    # If the user exists, check if the title already exists in the list
    current_titles = response['Item']['titles']
    if new_title in current_titles:
        return {
            'statusCode': 200,
            'body': json.dumps(current_titles)
        }

    # If the title does not exist in the list, append it and update the item
    current_titles.append(new_title)
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