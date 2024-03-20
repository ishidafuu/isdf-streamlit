import json
import os

from chat_app import ChatApp
from firebase_login import FirebaseLogin
from secret_manager import SecretManager

secrets_file_path = '../../secrets/secrets.json'
is_local = os.path.exists(secrets_file_path)


def get_local_anthropic_key():
    with open(secrets_file_path, 'r') as file:
        data = json.load(file)
    return data.get('anthropic-key')


def get_local_firebase_api_key():
    with open(secrets_file_path, 'r') as file:
        data = json.load(file)
    return data.get('firebase-api-key')


if is_local:
    # firebase_api_key = get_local_firebase_api_key()
    # if FirebaseLogin.login(firebase_api_key):
    anthropic_key = get_local_anthropic_key()
    app = ChatApp(anthropic_key)
    app.start_chat()

else:
    project_id = '955193391847'
    secret_manager = SecretManager(project_id)
    firebase_api_key = secret_manager.get_secret('firebase-api-key')

    if FirebaseLogin.login(firebase_api_key):
        anthropic_key = secret_manager.get_secret('anthropic-key')
        app = ChatApp(anthropic_key)
        app.start_chat()
