import json
import os
from datetime import timedelta

import pyrebase
import requests
import streamlit as st
from google.cloud import secretmanager

id_token_validity = timedelta(hours=24)
refresh_token_validity = timedelta(days=7)


class SecretManager:
    def __init__(self, project_id):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()
        self.secrets_file_path = '../../secrets/secrets.json'
        self.is_local = os.path.exists(self.secrets_file_path)
        with open(self.secrets_file_path, 'r') as file:
            self.data = json.load(file)

    def get_secret(self, secret_id):
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/latest"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode('UTF-8')

    def get_local_anthropic_key(self):
        return self.data.get('anthropic-key')

    def get_local_firebase_api_key(self):
        return self.data.get('firebase-api-key')


class FirebaseLogin:
    def __init__(self, firebase_api_key):
        self.firebase_api_key = firebase_api_key
        self.firebase = None
        self.auth = None
        self.initialize_firebase()

    def initialize_firebase(self):
        config = {
            "apiKey": self.firebase_api_key,
            "authDomain": "isdf-streamlit.firebaseapp.com",
            "storageBucket": "isdf-streamlit.appspot.com",
            "databaseURL": "https://isdf-streamlit.firebaseapp.com"
        }
        self.firebase = pyrebase.initialize_app(config)
        self.auth = self.firebase.auth()

    @staticmethod
    # @st.cache_data
    def is_logged_in():
        if "user_logged_in" not in st.session_state:
            st.session_state.user_logged_in = False

        return st.session_state.user_logged_in

    def login(self):
        if self.is_logged_in():
            return True

        email = st.empty()
        email = email.text_input("メールアドレスを入力してください")
        password = st.text_input("パスワードを入力してください", type="password")
        submit = st.button("ログイン")
        if submit and self.authenticate(email, password):
            st.session_state.user_logged_in = True
            st.cache_data.clear()
            st.experimental_rerun()
            return True
        return False

    def authenticate(self, email, password):
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            st.session_state.user = user
            return True

        except requests.exceptions.HTTPError as e:
            msg = json.loads(e.args[1])["error"]["message"]
            if msg == "EMAIL_NOT_FOUND" or msg == "INVALID_PASSWORD":
                st.error("メールアドレスかパスワードに誤りがあります。")
            elif msg == "USER_DISABLED":
                st.error("このユーザーは無効化されています。管理者にお問い合わせください。")
            elif msg == "TOO_MANY_ATTEMPTS_TRY_LATER":
                st.error("試行回数が多すぎます。しばらく経ってからお試しください。")
            else:
                st.error(f"ログインに失敗しました。{e}")

            if "user" in st.session_state:
                del st.session_state.user
            return False

    def refresh(self):
        if "user" not in st.session_state:
            return False
        try:
            user = self.auth.refresh(st.session_state.user["refreshToken"])
            st.session_state.user = user
            return True
        except Exception:
            del st.session_state.user
        return False
