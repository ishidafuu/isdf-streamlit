import streamlit as st

from firebase_auth import FirebaseAuth


class FirebaseLogin:
    @staticmethod
    @st.cache_data
    def is_logged_in():
        if "user_logged_in" not in st.session_state:
            st.session_state.user_logged_in = False

        return st.session_state.user_logged_in

    @staticmethod
    def login(firebase_api_key):
        if FirebaseLogin.is_logged_in():
            return True

        firebase_auth = FirebaseAuth(firebase_api_key)

        email = st.empty()
        email = email.text_input("メールアドレスを入力してください")
        password = st.text_input("パスワードを入力してください", type="password")
        submit = st.button("ログイン")
        if submit and firebase_auth.authenticate(email, password):
            st.session_state.user_logged_in = True
            st.cache_data.clear()
            st.experimental_rerun()
            return True
        return False
