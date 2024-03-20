import json
import os
from datetime import datetime, timedelta
from datetime import timezone
from typing import Optional

import requests
from dateutil.parser import parse
from firebase_admin import firestore, credentials, initialize_app

id_token_validity = timedelta(hours=24)
refresh_token_validity = timedelta(days=7)


class FirestoreTokenManager:
    def __init__(self):
        self.collection_auth = 'auth'
        self.document_id_token = 'id_token'
        self.document_refresh_token = 'refresh_token'
        self.field_id_token = 'id_token'
        self.field_refresh_token = 'refresh_token'
        self.field_retrieval_time = 'retrieval_time'
        self.document_user = 'user'
        self.field_mail_address = 'mail_address'
        self.field_password = 'password'

    def get_document(self, collection: str, document: str, field: str, validity: Optional[timedelta] = None) -> Optional[str]:
        db = firestore.client()
        doc = db.collection(collection).document(document).get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        if validity is not None:
            retrieval_time = data.get(self.field_retrieval_time)
            if retrieval_time is not None:
                retrieval_time = retrieval_time.replace(tzinfo=timezone.utc)
                if datetime.now(timezone.utc) - retrieval_time >= validity:
                    return None
        return data.get(field)

    def set_document(self, collection: str, document: str, fields: dict):
        db = firestore.client()
        data = fields
        data[self.field_retrieval_time] = datetime.now(timezone.utc)
        db.collection(collection).document(document).set(data)

    def get_refresh_token(self):
        return self.get_document(self.collection_auth, self.document_refresh_token, self.field_refresh_token,
                                 refresh_token_validity)

    def get_id_token(self):
        return self.get_document(self.collection_auth, self.document_id_token, self.field_id_token, id_token_validity)

    def set_refresh_token(self, refresh_token: str):
        self.set_document(self.collection_auth, self.document_refresh_token, {self.field_refresh_token: refresh_token})

    def set_id_token(self, id_token: str):
        self.set_document(self.collection_auth, self.document_id_token, {self.field_id_token: id_token})

    def get_mail_address(self):
        return self.get_document(self.collection_auth, self.document_user, self.field_mail_address)

    def get_password(self):
        return self.get_document(self.collection_auth, self.document_user, self.field_password)

    def upload_user_data(self, mail_address: str, password: str):
        # Firebase Admin SDKの初期化設定を行う
        cred = credentials.Certificate('firebase-adminsdk.json')
        initialize_app(cred)

        # FirebaseからFirestoreデータベースへの接続を確立する
        db = firestore.client()

        document = {
            self.field_mail_address: mail_address,
            self.field_password: password,
        }

        # 定義した文書をFirestoreの'tokens'コレクションの'refresh_token'ドキュメントに保存する
        db.collection(self.collection_auth).document(self.document_user).set(document)


class LocalTokenManager:
    def __init__(self):
        self.refresh_token = None
        self.refresh_token_retrieval_time = None
        self.id_token = None
        self.id_token_retrieval_time = None
        self.mail_address = None
        self.password = None
        self.file_path = '../../secrets/quants_key.json'
        self._load_from_file()

    def _load_from_file(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                self.refresh_token = data.get('refresh_token')
                self.id_token = data.get('id_token')
                self.mail_address = data.get('mail_address')
                self.password = data.get('password')

                refresh_token_retrieval_time = data.get('refresh_token_retrieval_time')
                if refresh_token_retrieval_time:
                    self.refresh_token_retrieval_time = parse(refresh_token_retrieval_time)
                else:
                    self.refresh_token_retrieval_time = None

                id_token_retrieval_time = data.get('id_token_retrieval_time')
                if id_token_retrieval_time:
                    self.id_token_retrieval_time = parse(id_token_retrieval_time)
                else:
                    self.id_token_retrieval_time = None
        except FileNotFoundError:
            print('トークンファイルが見つかりません。空の値で初期化しました。')

    def _save_to_file(self):
        data = {
            'refresh_token': self.refresh_token,
            'refresh_token_retrieval_time': self.refresh_token_retrieval_time.isoformat() if self.refresh_token_retrieval_time else None,
            'id_token': self.id_token,
            'id_token_retrieval_time': self.id_token_retrieval_time.isoformat() if self.id_token_retrieval_time else None,
            'mail_address': self.mail_address,
            'password': self.password
        }
        with open(self.file_path, 'w') as file:
            json.dump(data, file)

    def set_id_token(self, id_token: str):
        self.id_token = id_token
        self.id_token_retrieval_time = datetime.now()
        self._save_to_file()
        print('id_tokenを保存しました')

    def set_refresh_token(self, refresh_token: str):
        self.refresh_token = refresh_token
        self.refresh_token_retrieval_time = datetime.now()
        self._save_to_file()
        print('refresh_tokenを保存しました')

    def get_id_token(self):
        retrieval_time = getattr(self, 'id_token_retrieval_time', None)

        # retrieval_timeが存在しない場合、トークンの有効期限が切れている場合、またはトークンが空の場合、すぐにNoneを返します。
        if retrieval_time is None or datetime.now() - retrieval_time >= id_token_validity or not self.id_token:
            print('id_tokenを取得できませんでした')
            return None

        return self.id_token

    def get_refresh_token(self):
        retrieval_time = getattr(self, 'refresh_token_retrieval_time', None)

        # retrieval_timeが存在しない場合、トークンの有効期限が切れている場合、またはトークンが空の場合、すぐにNoneを返します。
        if retrieval_time is None or datetime.now() - retrieval_time >= refresh_token_validity or not self.refresh_token:
            print('retrieval_timeを取得できませんでした')
            return None

        return self.refresh_token

    def get_mail_address(self):
        return self.mail_address

    def get_password(self):
        return self.password


class TokenManager:
    def get_id_token_firebase(self):
        token_manager = FirestoreTokenManager()
        return self.get_id_token(token_manager)

    def get_id_token_local(self):
        token_manager = LocalTokenManager()
        return self.get_id_token(token_manager)

    def get_id_token(self, token_manager):
        id_token = token_manager.get_id_token()

        if id_token is None:
            refresh_token = token_manager.get_refresh_token()
            if refresh_token is None:
                mail_address = token_manager.get_mail_address()
                password = token_manager.get_password()
                refresh_token = self.call_token_auth_user(mail_address, password)
                print(refresh_token)
                print(f"refresh_token:{refresh_token}")
                token_manager.set_refresh_token(refresh_token)

            id_token = self.call_token_auth_refresh(refresh_token)
            print(f"id_token:{id_token}")
            token_manager.set_id_token(id_token)

        return id_token

    def upload_user_data_to_firebase(self):
        firebase_token_manager = FirestoreTokenManager()
        local_token_manager = LocalTokenManager()

        mail_address = local_token_manager.get_mail_address()
        password = local_token_manager.get_password()
        firebase_token_manager.upload_user_data(mail_address, password)

    @staticmethod
    def call_token_auth_user(mail_address: str, password: str):
        url = "https://api.jquants.com/v1/token/auth_user"
        data = {"mailaddress": mail_address, "password": password}
        if os.getenv("ENV") == "test":
            print("start")
            print(url)
            print(data)

        # 送信するデータを作成します。
        # トークンの認証ユーザーエンドポイントにPOSTリクエストを送信します。
        res = requests.post(url, data=json.dumps(data))

        if res.status_code != 200:
            res_json = res.json()
            message = res_json.get('message', 'No error message returned')
            raise RuntimeError(f"RefreshTokenの取得に失敗しました: {message}")

        # 取得したリフレッシュトークンを返します。
        return res.json()['refreshToken']

    @staticmethod
    def call_token_auth_refresh(refresh_token: str):
        url = f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={refresh_token}"
        if os.getenv("ENV") == "test":
            print("start")
            print(url)

        res = requests.post(url)

        if res.status_code != 200:
            res_json = res.json()
            message = res_json.get('message', 'No error message returned')
            raise RuntimeError(f"{url}:{message}")

        id_token = res.json()['idToken']
        return id_token
