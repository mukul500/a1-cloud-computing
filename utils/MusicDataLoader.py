import boto3
import json

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('music')


# Function to put items into DynamoDB table
def put_items(songs):
    for song in songs['songs']:
        title = song['title']
        artist = song['artist']
        year = song['year']
        web_url = song['web_url']
        image_url = f"s3://{bucket_name}/{song['img_s3_key']}"

        # Put item into DynamoDB table
        table.put_item(
            Item={
                'title': title,
                'artist': artist,
                'year': year,
                'web_url': web_url,
                'image_url': image_url
            }
        )


bucket_name = 's3959662Images'
# Load JSON data with S3 keys

with open('../songs_with_s3_keys.json', 'r') as f:
    songs_data = json.load(f)

# Put items into DynamoDB table
put_items(songs_data)