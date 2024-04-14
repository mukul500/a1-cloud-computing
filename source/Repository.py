import boto3
import requests

api_url = "https://skbc0bw6kd.execute-api.us-east-1.amazonaws.com/stage/"


def get_user(email):
    user_url = api_url + "user"
    params = {'email': email}
    response = requests.get(user_url, params=params)
    print(response)
    if response.status_code == 200:
        return response.json()
    return None


def query_music(title, artist, year):
    music_url = api_url + "queryMusic"
    params = {'artist': ''}
    if title:
        params = {'title': title}
    if artist:
        params = {'artist': artist}
    if year:
        params = {'year': year}
    response = requests.get(music_url, params=params)
    return response.json()


def register_user(email, username, password):
    user_url = api_url + "user"
    data = {'email': email, 'username': username, 'password': password}
    response = requests.post(user_url, params=data)
    if response.status_code == 200:
        return True
    return response.json()


def get_subscribed_music(email):
    print(email)
    subscribed_music_url = api_url + "subscribed-music"
    data = {'email': email}
    response = requests.get(subscribed_music_url, params=data)
    print(response.json())
    return response.json()


def add_subscribed_music(email, title):
    music_url = api_url + "subscribeMusic"
    data = {'email': email, 'new_title': title}
    response = requests.get(music_url, params=data)
    print(response.json())
    return response.json()


def remove_subscribed_music(email, title):
    music_url = api_url + "removeSubscribeMusic"
    data = {'email': email, 'remove': title}
    response = requests.get(music_url, params=data)
    return response.json()
