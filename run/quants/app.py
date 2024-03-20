from chat_app import ChatApp
from common import SecretManager
from token_manager import TokenManager

project_id = '955193391847'
secret_manager = SecretManager(project_id)

token_manager = TokenManager()
if secret_manager.is_local:
    anthropic_key = secret_manager.get_local_anthropic_key()
    id_token = token_manager.get_id_token_local()
else:
    anthropic_key = secret_manager.get_secret('anthropic-key')
    id_token = token_manager.get_id_token_firebase()

app = ChatApp(anthropic_key, id_token)
app.start_chat()
