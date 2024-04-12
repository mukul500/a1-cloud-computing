import boto3
import json
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('music')


def lambda_handler(event, context):
    # Extract query parameters from the event
    title = event.get('title')
    artist = event.get('artist')
    year = event.get('year')

    print(title, artist, year)
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
        return response.get('Items', [])

    # Construct the filter expression string
    filter_expression_str = ' AND '.join(filter_expression)
    print(filter_expression_str)
    # Execute the query
    response = table.scan(
        FilterExpression=filter_expression_str,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values
    )
    print(filter_expression_str, expression_attribute_names, expression_attribute_values)

    # Extract the list of music items from the response
    music_list = response.get('Items', [])

    if not music_list:
        return {
            'statusCode': 400,
            'body': json.dumps('No music items found')
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps(music_list)
        }

