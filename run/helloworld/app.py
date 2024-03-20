from chat_app import ChatApp
from common import SecretManager

project_id = '955193391847'
secret_manager = SecretManager(project_id)

# if secret_manager.is_local():
#     anthropic_key = secret_manager.get_local_anthropic_key()
#     app = ChatApp(anthropic_key)
#     app.start_chat()
#
# else:
#     firebase_api_key = secret_manager.get_secret('firebase-api-key')
#     if FirebaseLogin.login(firebase_api_key):
#         anthropic_key = secret_manager.get_secret('anthropic-key')
#         app = ChatApp(anthropic_key)
#         app.start_chat()


anthropic_key = secret_manager.get_secret('anthropic-key')
app = ChatApp(anthropic_key)
app.start_chat()
