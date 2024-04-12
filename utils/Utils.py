import boto3

from source.Repository import get_user
from source import Repository

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
user_table = dynamodb.Table('login')


# def get_user(email):
#     response = user_table.get_item(Key={'email': email})
#     return response.get('Item')


def verify_user(email, password):
    user = get_user(email)
    if user is None:
        return False
    if not user or user['password'] != password:
        return False
    return True


def user_exists(email):
    return True if get_user(email) else False


def register_user(email, username, password):
    user_table.put_item(Item={'email': email, 'username': username, 'password': password})


def query_music(title, artist, year):
    return Repository.query_music(title, artist, year)


def get_subscribed_music(email):
    return Repository.get_subscribed_music(email)


def add_subscribed_music(email, title):
    return Repository.add_subscribed_music(email, title)


def remove_subscribed_music(email, title):
    return Repository.remove_subscribed_music(email, title)

