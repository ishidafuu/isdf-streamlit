import anthropic
import streamlit as st
from google.cloud import secretmanager

#  gcloud run deploy helloworld --region "asia-northeast1" --source .
def get_api_key_from_secret_manager(project_id, secret_id):
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    # Access the secret.
    response = client.access_secret_version(request={"name": name})

    # Return the decoded payload of the secret.
    return response.payload.data.decode('UTF-8')


# Use the function to get API key
project_id = '955193391847'  # replace with your project id
secret_id = 'anthropic-key'  # replace with your secret id
anthropic_key = get_api_key_from_secret_manager(project_id, secret_id)

# AntrhopicClientを初期化
client = anthropic.Anthropic(api_key=anthropic_key)

# # タイトルを設定
st.title("Claude3 by Streamlit")

# セッション内のメッセージが指定されていない場合のデフォルト値
if "messages" not in st.session_state:
    st.session_state.messages = []

# 以前のメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの新しい入力を取得
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response_message = ""
        with client.messages.stream(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
        ) as stream:
            for text in stream.text_stream:
                response_message += text
                message_placeholder.markdown(response_message)

    final_message = stream.get_final_message()
    input_token = final_message.usage.input_tokens
    output_token = final_message.usage.output_tokens
    message_placeholder.markdown(f"{response_message} \n token:{input_token + output_token} (i:{input_token} o:{output_token})")
    st.session_state.messages.append({"role": "assistant", "content": response_message})
