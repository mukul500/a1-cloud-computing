import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('music')


def lambda_handler(event, context):
    # Extract query parameters from the event

    # Extract query parameters from the event
    title = None
    artist = None
    year = None

    if event.get('queryStringParameters') is not None:
        title = event.get('queryStringParameters').get('title')
        artist = event.get('queryStringParameters').get('artist')
        year = event.get('queryStringParameters').get('year')

    # Construct the filter expression and expression attribute values for the query
    filter_expression = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    if title:
        filter_expression.append('contains(#title, :title)')
        expression_attribute_values[':title'] = title
        expression_attribute_names['#title'] = 'title'
    if artist:
        filter_expression.append('contains(#artist, :artist)')
        expression_attribute_values[':artist'] = artist
        expression_attribute_names['#artist'] = 'artist'
    if year:
        filter_expression.append('#year = :year')
        expression_attribute_values[':year'] = year
        expression_attribute_names['#year'] = 'year'

    # If no query parameters are provided, return all music items
    if not (title or artist or year):
        response = table.scan()

        music_list = response.get('Items', [])
        limited_music_list = get_music_with_signed_url(music_list[:15])
        return {
            'statusCode': 200,
            'body': json.dumps(limited_music_list)
        }

    # Construct the filter expression string
    filter_expression_str = ' AND '.join(filter_expression)
    # Execute the query
    response = table.scan(
        FilterExpression=filter_expression_str,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values
    )

    # Extract the list of music items from the response
    music_list = response.get('Items', [])
    limited_music_list = get_music_with_signed_url(music_list[:15])

    if not music_list:
        return {
            'statusCode': 200,
            'body': json.dumps([])
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps(limited_music_list)
        }


def get_music_with_signed_url(music):
    s3_client = boto3.client('s3', region_name='us-east-1')

    for song in music:
        print(song)
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': 's3959662images',
                'Key': song['image_url']
            },
            ExpiresIn=3600
        )
        song['image_url'] = url
    return music