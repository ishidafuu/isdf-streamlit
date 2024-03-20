import anthropic
import streamlit as st


class ChatApp:
    def __init__(self, anthropic_key):
        self.anthropic_key = anthropic_key
        self.messages = []
        self.model_options = ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"]
        self.model = self.model_options[0]

    def start_chat(self):
        with st.sidebar:
            self.model = st.radio("Select a model", self.model_options, index=self.model_options.index(self.model))

        # AntrhopicClientを初期化
        client = anthropic.Anthropic(api_key=self.anthropic_key)

        # タイトルを設定
        st.title(f"{self.model}")

        # 以前のメッセージを表示
        for message in self.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # ユーザーからの新しい入力を取得
        if prompt := st.chat_input("What is up?"):
            self.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                response_message = ""
                with client.messages.stream(
                        model=self.model,
                        max_tokens=1024,
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in self.messages
                        ]
                ) as stream:
                    for text in stream.text_stream:
                        response_message += text
                        message_placeholder.markdown(response_message)

            final_message = stream.get_final_message()
            input_token = final_message.usage.input_tokens
            output_token = final_message.usage.output_tokens
            message_placeholder.markdown(f"{response_message} \n token:{input_token + output_token} (i:{input_token} o:{output_token})")
            self.messages.append({"role": "assistant", "content": response_message})
