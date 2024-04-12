import boto3
import requests

api_url = "https://c9ovkz7jre.execute-api.us-east-1.amazonaws.com/stage/"


def get_user(email):
    user_url = api_url + "user"
    params = {'email': email}
    response = requests.get(user_url, params=params)
    return response.json()


def query_music(title, artist, year):
    music_url = api_url + "music"
    params = {'title': title, 'artist': artist, 'year': year}
    response = requests.get(music_url, params=params)
    return response.json()


def register_user(email, username, password):
    user_url = api_url + "user"
    data = {'email': email, 'username': username, 'password': password}
    response = requests.post(user_url, params=data)
    return response.json()


def get_subscribed_music(email):
    print(email)
    subscribed_music_url = api_url + "subscribed-music"
    data = {'email': email}
    response = requests.get(subscribed_music_url, params=data)
    print(response.json())
    return response.json()


def add_subscribed_music(email, title):
    music_url = api_url + "subscribed"
    data = {'email': email, 'title': title}
    response = requests.post(music_url, params=data)
    return response.json()


def remove_subscribed_music(email, title):
    music_url = api_url + "subscribed"
    data = {'email': email, 'title': title}
    response = requests.delete(music_url, params=data)
    return response.json()
