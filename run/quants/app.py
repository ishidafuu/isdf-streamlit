import streamlit as st

from chat_app import ChatApp
from common import SecretManager, FirebaseLogin
from token_manager import TokenManager

project_id = '955193391847'
secret_manager = SecretManager(project_id)


@st.cache_data
def get_id_token_firebase():
    token_manager = TokenManager()
    return token_manager.get_id_token_firebase()


if secret_manager.is_local:
    anthropic_key = secret_manager.get_local_anthropic_key()
    token_manager = TokenManager()
    id_token = token_manager.get_id_token_local()
    app = ChatApp(anthropic_key, id_token, True)
    app.start_chat()

else:
    firebase_api_key = secret_manager.get_secret('firebase-api-key')
    firebase_login = FirebaseLogin(firebase_api_key)
    if firebase_login.login():
        anthropic_key = secret_manager.get_secret('anthropic-key')
        id_token = get_id_token_firebase()
        app = ChatApp(anthropic_key, id_token, False)
        app.start_chat()
