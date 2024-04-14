import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('subscriptions')
music_table = dynamodb.Table('music')


def lambda_handler(event, context):
    # Extract the user's email from the event
    subscribed_music_details = []
    email = event.get('queryStringParameters', {}).get('email')

    # Get the list of subscribed titles for the user from the SubscriptionTable
    response = table.get_item(
        Key={'email': email}
    )

    if 'Item' not in response:
        return {
            'statusCode': 200,
            'body': json.dumps(subscribed_music_details)
        }

    subscribed_titles = response['Item'].get('titles', [])

    # Retrieve details of subscribed titles from the MusicTable

    for title in subscribed_titles:
        music_response = music_table.get_item(
            Key={'title': title}
        )
        if 'Item' in music_response:
            music_details = music_response['Item']
            subscribed_music_details.append({
                'title': music_details['title'],
                'year': music_details['year'],
                'image_url': get_signed_url(music_details['image_url'])
            })

    return {
        'statusCode': 200,
        'body': json.dumps(subscribed_music_details)
    }


def get_signed_url(unsignedUrl):
    s3_client = boto3.client('s3', region_name='us-east-1')
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': 's3959662images',
            'Key': unsignedUrl
        },
        ExpiresIn=3600
    )
    return url