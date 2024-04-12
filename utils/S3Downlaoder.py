import json
import uuid

import boto3
import requests


# Function to generate a unique key for the image
def generate_unique_key(title, artist):
    # Generate a random UUID
    unique_id = uuid.uuid4().hex
    # Construct the key using title, artist, and unique_id
    key = f"{artist}_{title}_{unique_id}.jpg"
    return key


# Function to download and upload images to S3
def process_images(songs):
    s3 = boto3.client('s3')

    for song in songs['songs']:
        title = song['title']
        artist = song['artist']
        img_url = song['img_url']

        # Download image
        response = requests.get(img_url)
        if response.status_code == 200:
            # Generate unique key for the image
            img_key = generate_unique_key(title, artist)
            # Upload image to S3
            img_data = response.content
            s3.put_object(Bucket='s3959662images', Key=img_key, Body=img_data)

            # Save S3 key to JSON
            song['img_s3_key'] = img_key

    # Save modified JSON to local file
    with open('../songs_with_s3_keys.json', 'w') as f:
        json.dump(songs, f, indent=2)


# Load JSON data
with open('../a1.json', 'r') as f:
    songs_data = json.load(f)

# Process images and update JSON
process_images(songs_data)