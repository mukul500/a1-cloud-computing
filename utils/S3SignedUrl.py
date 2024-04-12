import boto3


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
