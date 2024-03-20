import json

import pyrebase
import requests
import streamlit as st


class FirebaseAuth:
    def __init__(self, firebase_api_key: str):
        self.firebase_api_key = firebase_api_key
        self.firebase = None
        self.auth = None

    def authenticate(self, email: str, password: str):
        try:
            config = {
                "apiKey": self.firebase_api_key,
                "authDomain": "isdf-streamlit.firebaseapp.com",
                "storageBucket": "isdf-streamlit.appspot.com",
                "databaseURL": "https://isdf-streamlit.firebaseapp.com"
            }

            self.firebase = pyrebase.initialize_app(config)
            self.auth = self.firebase.auth()

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
